import argparse
import pandas as pd
import numpy as np
import yaml
import json
import logging
import time
import sys
import os


def setup_logger(log_file):
    """
    Configure logging to write to file with INFO level.
    Ensures logs persist even if stdout/stderr is redirected.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode='w'
    )


def write_metrics(output_path, data):
    """
    Write metrics to JSON file ensuring parent directory exists.
    FIX #8: Ensures metrics.json is written even in failure cases.
    """
    try:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to write metrics to {output_path}: {str(e)}")
        raise


def main(args):
    start_time = time.time()
    metrics = None

    try:
        logging.info("=" * 60)
        logging.info("MLOps Batch Pipeline - Job Started")
        logging.info("=" * 60)

        # ============================
        # 1. Load and validate config
        # ============================
        if not os.path.exists(args.config):
            raise FileNotFoundError(f"Config file not found: {args.config}")

        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        required_keys = ["seed", "window", "version"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        # FIX #6: Ensure determinism with numpy seed
        np.random.seed(seed)
        logging.info(f"Configuration loaded: seed={seed}, window={window}, version={version}")

        # ============================
        # 2. Load dataset (FIX #1)
        # ============================
        if not os.path.exists(args.input):
            raise FileNotFoundError(f"Input file not found: {args.input}")

        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("Dataset is empty")

        if "close" not in df.columns:
            raise ValueError("Missing 'close' column in dataset")

        total_rows_before = len(df)
        logging.info(f"Dataset loaded successfully: {total_rows_before} total rows")

        # ============================
        # 3. Compute rolling mean (FIX #3)
        # ============================
        # FIX #3: Use df["close"].rolling(window).mean() and drop NaN rows
        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        
        # Drop NaN rows (first window-1 rows from rolling window)
        df = df.dropna(subset=["rolling_mean"])
        
        rows_after_rolling = len(df)
        rows_dropped = total_rows_before - rows_after_rolling
        logging.info(f"Rolling mean computed: {rows_dropped} NaN rows dropped (window={window})")
        logging.info(f"Rows after rolling window processing: {rows_after_rolling}")

        # ============================
        # 4. Generate signal
        # ============================
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
        logging.info("Signal generation completed")

        # ============================
        # 5. Calculate metrics (FIX #1, #2, #5)
        # ============================
        rows_processed = len(df)
        signal_count = df["signal"].sum()
        
        # FIX #2: Ensure signal_rate is decimal (not percentage)
        # FIX #2: Round to 4 decimal places
        signal_rate = df["signal"].mean()
        signal_rate_rounded = round(signal_rate, 4)
        
        latency_ms = int((time.time() - start_time) * 1000)

        # FIX #5: Enhanced logging for signal_rate and rows_processed
        logging.info(f"Total rows processed: {rows_processed}")
        logging.info(f"Signal events detected: {signal_count}")
        logging.info(f"Signal rate (decimal): {signal_rate_rounded} (0.0 to 1.0 range)")
        logging.info(f"Execution latency: {latency_ms} ms")

        # ============================
        # 6. Build metrics (FIX #4)
        # ============================
        # FIX #4: Ensure metrics JSON format EXACTLY matches required format
        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": signal_rate_rounded,  # Decimal format, rounded to 4 places
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        logging.info("=" * 60)
        logging.info(f"Metrics Summary: {json.dumps(metrics, indent=2)}")
        logging.info("Job completed successfully")
        logging.info("=" * 60)

        write_metrics(args.output, metrics)
        print(json.dumps(metrics, indent=2))
        sys.exit(0)

    except Exception as e:
        logging.error("=" * 60)
        logging.error(f"Pipeline Error: {str(e)}")
        logging.error("=" * 60)

        # FIX #8: Write error metrics to ensure metrics.json exists even on failure
        error_metrics = {
            "version": "v1" if not metrics else metrics.get("version", "v1"),
            "status": "error",
            "error_message": str(e)
        }

        try:
            write_metrics(args.output, error_metrics)
        except Exception as write_err:
            logging.error(f"Failed to write error metrics: {str(write_err)}")

        print(json.dumps(error_metrics, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="MLOps Batch Pipeline - Processes financial data with rolling mean signal generation"
    )

    parser.add_argument("--input", required=True, help="Path to input CSV file (must contain 'close' column)")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument("--output", required=True, help="Path to output metrics JSON file")
    parser.add_argument("--log-file", required=True, help="Path to log file")

    args = parser.parse_args()

    setup_logger(args.log_file)
    main(args)
