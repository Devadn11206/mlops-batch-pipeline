# MLOps Task

A machine learning operations pipeline for model training and evaluation.

## Project Structure

```
mlops-task/
├── run.py          # Main pipeline execution script
├── config.yaml     # Configuration file
├── data.csv        # Training data
├── requirements.txt # Python dependencies
├── Dockerfile      # Docker container specification
├── README.md       # This file
├── metrics.json    # Output metrics
└── run.log         # Execution logs
```

## Setup

### Prerequisites
- Python 3.11+
- Docker (optional)
- pip or conda

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the pipeline by editing `config.yaml`

## Usage

### Local Execution
```bash
python run.py
```

### Docker Execution
```bash
docker build -t mlops-task .
docker run mlops-task
```

## Configuration

Edit `config.yaml` to customize:
- Model type and hyperparameters
- Training parameters
- Input/output paths
- Metrics output

## Output

- `metrics.json` - Model evaluation metrics
- `run.log` - Execution logs and debug information

## License

MIT
