# Lightreel Video Downloader

Download 184k+ videos from lightreel.ai metadata and upload to S3.

## Requirements

- Python 3.8+
- AWS CLI configured
- 32GB+ RAM recommended for parallel processing
- Internet connection

## Quick Start (Windows / Linux / Mac)

### 1. Install Dependencies

```bash
# Clone the repo
git clone https://github.com/shoezaz/lightreel-downloader
cd lightreel-downloader

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure AWS

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter default region name: eu-west-3
# Enter default output format: json
```

Or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=eu-west-3
```

### 3. Run the Downloader

**Parallel version (recommended - 32 workers):**
```bash
python download_parallel.py
```

**Single-threaded version (slower but stable):**
```bash
python download.py
```

## Progress Tracking

Check how many videos are already downloaded:
```bash
aws s3 ls s3://lightreel-videos-prod-001/videos/ --region eu-west-3 | wc -l
```

## Configuration

Edit these variables in the scripts if needed:

| Variable | Default | Description |
|----------|---------|-------------|
| `S3_BUCKET` | lightreel-videos-prod-001 | Your S3 bucket |
| `S3_PREFIX` | videos | S3 prefix for videos |
| `JSON_KEY` | data/lightreel_all_videos.json | JSON file with video metadata |
| `MAX_WORKERS` | 32 | Number of parallel downloads |

## Windows-Specific

### Install AWS CLI on Windows

```powershell
# Using Winget (recommended)
winget install Amazon.AWSCLIV2

# Or download directly
# https://awscli.amazonaws.com/AWSCLIV2.msi
```

### Install Python dependencies

```powershell
pip install -r requirements.txt
```

### Run

```powershell
python download_parallel.py
```

## Linux-Specific

### Install dependencies

```bash
sudo apt update
sudo apt install python3-pip awscli
pip3 install -r requirements.txt
```

### Run

```bash
python3 download_parallel.py
```

## Performance Tips

1. **More workers = faster**: Increase `MAX_WORKERS` to 64 or 128 if you have a powerful CPU
2. **Check bandwidth**: Make sure you have a fast internet connection
3. **Resume capability**: The script automatically skips already downloaded videos

## Troubleshooting

### "Unable to locate credentials"

Make sure AWS is configured:
```bash
aws configure
```

Or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### "Connection timeout"

The script has a 60-second timeout per video. If you have slow internet, you can increase it in the code.

### Videos not uploading to S3

Make sure your IAM user has S3 permissions:
```json
{
  "Effect": "Allow",
  "Action": ["s3:PutObject", "s3:ListBucket"],
  "Resource": ["arn:aws:s3:::lightreel-videos-prod-001", "arn:aws:s3:::lightreel-videos-prod-001/*"]
}
```

## License

MIT
