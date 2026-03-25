# Lightreel Video Downloader

Download 184k videos from lightreel.ai metadata and upload to S3.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS
aws configure
# Enter your AWS credentials and region (eu-west-3)
```

## Run

### Single-threaded (slower but stable)
```bash
python download.py
```

### Parallel (faster, recommended)
```bash
python download_parallel.py
```

## Configuration

Edit these variables in the script:
- `S3_BUCKET`: "lightreel-videos-prod-001"
- `S3_PREFIX`: "videos"  
- `JSON_KEY`: "data/lightreel_all_videos.json"
- `MAX_WORKERS`: 32 (adjust based on your CPU)

## Progress

The script tracks which videos are already downloaded and skips them.
Check progress:
```bash
aws s3 ls s3://lightreel-videos-prod-001/videos/ | wc -l
```
