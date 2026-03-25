#!/usr/bin/env python3
"""
Lightreel Video Downloader
Downloads videos from JSON metadata and uploads to S3

Usage:
    export AWS_ACCESS_KEY_ID=your_key
    export AWS_SECRET_ACCESS_KEY=your_secret
    export AWS_REGION=eu-west-3
    python download.py
"""
import boto3
import requests
import json
import os
import sys

S3_BUCKET = "lightreel-videos-prod-001"
S3_PREFIX = "videos"
JSON_KEY = "data/lightreel_all_videos.json"

def main():
    print("[START] Lightreel Video Downloader")
    
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
        print(f"Error listing: {e}")
    
    print(f"Already downloaded: {len(downloaded)}")
    
    to_download = [v for v in videos if v.get("_id") and v.get("videoUrl") and v["_id"] not in downloaded]
    print(f"Need to download: {len(to_download)}")
    
    if not to_download:
        print("All videos already downloaded!")
        return
    
    success = 0
    failed = 0
    
    for i, video in enumerate(to_download):
        vid_id = video.get("_id")
        video_url = video.get("videoUrl")
        
        if (i + 1) % 10 == 0:
            print(f"[{i+1}/{len(to_download)}] Downloading {vid_id}...")
        
        try:
            r = requests.get(video_url, timeout=60)
            if r.status_code == 200:
                s3.put_object(
                    Bucket=S3_BUCKET,
                    Key=f"{S3_PREFIX}/{vid_id}.mp4",
                    Body=r.content,
                    ContentType="video/mp4"
                )
                success += 1
            else:
                failed += 1
        except Exception as e:
            failed += 1
            if failed % 10 == 0:
                print(f"Failed: {failed}")
    
    print(f"\n[DONE] Success: {success}, Failed: {failed}")

if __name__ == "__main__":
    main()
