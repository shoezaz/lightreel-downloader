# Lightreel Video Downloader

Download 184k+ videos from lightreel.ai metadata and upload to S3.

## Requirements

- Python 3.8+
- Internet connection

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/shoezaz/lightreel-downloader
cd lightreel-downloader
pip install -r requirements.txt
```

### 2. Set AWS Credentials

**Option A - Environment variables (recommended):**
```bash
# Linux/Mac
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=eu-west-3
export MAX_WORKERS=32  # optional, default 32
```

**Option B - AWS CLI:**
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region name: eu-west-3
# Default output format: json
```

### 3. Run

```bash
python download_parallel.py
```

## Performance

- **Parallel version** (`download_parallel.py`): 32+ workers, recommended for fast download
- **Single version** (`download.py`): 1 worker, slower but more stable

Increase workers for faster download:
```bash
export MAX_WORKERS=64
python download_parallel.py
```

## Progress Tracking

Check downloaded videos:
```bash
aws s3 ls s3://lightreel-videos-prod-001/videos/ --region eu-west-3 | wc -l
```

## Troubleshooting

### Credentials error
Make sure AWS credentials are set:
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=eu-west-3
```

### Slow download
Increase MAX_WORKERS:
```bash
export MAX_WORKERS=64
python download_parallel.py
```

## License

MIT
