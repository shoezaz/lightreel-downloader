#!/usr/bin/env python3
"""
Lightreel Video Downloader - Parallel Version
Uses multiprocessing for faster downloads

Usage:
    export AWS_ACCESS_KEY_ID=your_key
    export AWS_SECRET_ACCESS_KEY=your_secret
    export AWS_REGION=eu-west-3
    python download_parallel.py
"""
import boto3
import requests
import json
import os
from multiprocessing import Pool

S3_BUCKET = "lightreel-videos-prod-001"
S3_PREFIX = "videos"
JSON_KEY = "data/lightreel_all_videos.json"
MAX_WORKERS = int(os.environ.get("MAX_WORKERS", "32"))

def download_video(args):
    """Download a single video"""
    vid_id, video_url, bucket, prefix = args
    
    try:
        r = requests.get(video_url, timeout=60)
        if r.status_code == 200:
            s3 = boto3.client("s3")
            s3.put_object(
                Bucket=bucket,
                Key=f"{prefix}/{vid_id}.mp4",
                Body=r.content,
                ContentType="video/mp4"
            )
            return vid_id, True
    except Exception as e:
        pass
    return vid_id, False

def main():
    print(f"[START] Lightreel Parallel Downloader ({MAX_WORKERS} workers)")
    
    s3 = boto3.client("s3")
    
    print("Loading videos from S3...")
    resp = s3.get_object(Bucket=S3_BUCKET, Key=JSON_KEY)
    videos = json.loads(resp["Body"].read().decode("utf-8"))
    print(f"Total videos in JSON: {len(videos)}")
    
    print("Getting already downloaded videos...")
    downloaded = set()
    try:
        resp = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_PREFIX)
        for obj in resp.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".mp4"):
                vid_id = key.replace(S3_PREFIX + "/", "").replace(".mp4", "")
                downloaded.add(vid_id)
    except Exception as e:
        print(f"Note: {e}")
    
    print(f"Already downloaded: {len(downloaded)}")
    
    to_download = [
        (v["_id"], v["videoUrl"], S3_BUCKET, S3_PREFIX)
        for v in videos
        if v.get("_id") and v.get("videoUrl") and v["_id"] not in downloaded
    ]
    print(f"Need to download: {len(to_download)}")
    
    if not to_download:
        print("All videos already downloaded!")
        return
    
    success = 0
    failed = 0
    
    with Pool(processes=MAX_WORKERS) as pool:
        results = pool.map(download_video, to_download)
        for vid_id, ok in results:
            if ok:
                success += 1
                if success % 100 == 0:
                    print(f"Progress: {success}/{len(to_download)}")
            else:
                failed += 1
    
    print(f"\n[DONE] Success: {success}, Failed: {failed}")

if __name__ == "__main__":
    main()
