# Lightreel Video Downloader

Download 184k+ videos from lightreel.ai metadata and upload to S3.

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/shoezaz/lightreel-downloader
cd lightreel-downloader
pip install -r requirements.txt
```

### 2. Configure AWS

**Option A - Environment variables:**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=eu-west-3
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

Default: 32 workers. Increase for faster download:
```bash
export MAX_WORKERS=64
python download_parallel.py
```

## Progress

Check downloaded videos:
```bash
aws s3 ls s3://lightreel-videos-prod-001/videos/ --region eu-west-3 | wc -l
```

## License

MIT
