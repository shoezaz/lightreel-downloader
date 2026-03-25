# Lightreel Video Downloader

Download 184k+ videos from lightreel.ai metadata and upload to S3.

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/shoezaz/lightreel-downloader
cd lightreel-downloader
pip install -r requirements.txt
```

### 2. Run

Credentials are in `.env` file (auto-loaded):

```bash
python download_parallel.py
```

## Progress

Check downloaded videos:
```bash
aws s3 ls s3://lightreel-videos-prod-001/videos/ --region eu-west-3 | wc -l
```

## License

MIT
