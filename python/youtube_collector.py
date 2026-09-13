"""
youtube_collector.py
────────────────────
YouTube Data API v3 コレクタースクリプト

対象:
  - チャンネルメタデータ
  - アップロード動画リスト
  - 動画ごとの統計・メタデータ
  - トップレベルコメント

出力:
  - data/channel_info.json
  - data/videos.csv  /  data/videos.json
  - data/comments.csv  /  data/comments.json

必要な環境変数（.env ファイルまたは実行環境で設定）:
  YOUTUBE_API_KEY=<APIキー>
  YOUTUBE_CHANNEL_ID=<チャンネルID>  # 例: UCxxxxxxxxxxxxxx

使い方:
  pip install -r requirements.txt
  python youtube_collector.py

注意:
  YouTube Data API v3 の無料クォータは 1日 10,000 ユニットです。
  大量の動画を持つチャンネルを取得する場合はクォータを確認してください。
"""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─────────────────────────────────────────
# 設定
# ─────────────────────────────────────────
load_dotenv()

API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
CHANNEL_ID: str = os.getenv("YOUTUBE_CHANNEL_ID", "")
MAX_COMMENTS_PER_VIDEO: int = int(os.getenv("MAX_COMMENTS_PER_VIDEO", "100"))
OUTPUT_DIR: Path = Path("data")

# ─────────────────────────────────────────
# ユーティリティ
# ─────────────────────────────────────────

def now_jst() -> str:
    """現在時刻を ISO 8601 文字列で返す（UTC）。分析データの取得タイムスタンプとして使用する。"""
    return datetime.now(timezone.utc).isoformat()


def duration_seconds(iso_duration: str) -> int:
    """ISO 8601 の duration 文字列を秒数に変換する。例: PT1M30S → 90"""
    try:
        return int(isodate.parse_duration(iso_duration).total_seconds())
    except Exception:
        return 0


def is_shorts(duration_sec: int) -> bool:
    """60 秒以下の動画を Shorts と判定する。"""
    return 0 < duration_sec <= 60


def save_json(data: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[保存] {path}")


def save_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        print(f"[スキップ] データが空のため {path} は作成しません。")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"[保存] {path}")


# ─────────────────────────────────────────
# チャンネル情報の取得
# ─────────────────────────────────────────

def fetch_channel_info(youtube, channel_id: str) -> dict:
    """チャンネルメタデータと統計を取得する。"""
    response = youtube.channels().list(
        part="snippet,statistics,contentDetails,brandingSettings",
        id=channel_id,
    ).execute()

    items = response.get("items", [])
    if not items:
        raise ValueError(f"チャンネルが見つかりません: {channel_id}")

    item = items[0]
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    content = item.get("contentDetails", {})
    branding = item.get("brandingSettings", {}).get("channel", {})

    return {
        "channel_id": item["id"],
        "title": snippet.get("title", ""),
        "description": snippet.get("description", ""),
        "published_at": snippet.get("publishedAt", ""),
        "country": snippet.get("country", ""),
        "keywords": branding.get("keywords", ""),
        "subscriber_count": int(stats.get("subscriberCount", 0)),
        "view_count": int(stats.get("viewCount", 0)),
        "video_count": int(stats.get("videoCount", 0)),
        "uploads_playlist_id": content.get("relatedPlaylists", {}).get("uploads", ""),
        "fetched_at": now_jst(),
    }


# ─────────────────────────────────────────
# 動画 ID リストの取得
# ─────────────────────────────────────────

def fetch_video_ids(youtube, uploads_playlist_id: str) -> list[str]:
    """アップロードプレイリストから全動画 ID を取得する。"""
    video_ids: list[str] = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        ).execute()

        for item in response.get("items", []):
            vid = item.get("contentDetails", {}).get("videoId")
            if vid:
                video_ids.append(vid)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    print(f"[取得] 動画ID: {len(video_ids)} 件")
    return video_ids


# ─────────────────────────────────────────
# 動画詳細（メタデータ + 統計）の取得
# ─────────────────────────────────────────

def fetch_video_details(youtube, video_ids: list[str]) -> list[dict]:
    """動画 ID リストを 50 件ずつ分割して詳細を取得する。"""
    details: list[dict] = []
    fetched_at = now_jst()

    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i : i + 50]
        response = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(chunk),
        ).execute()

        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})

            duration_sec = duration_seconds(content.get("duration", "PT0S"))
            title = snippet.get("title", "")

            details.append({
                "video_id": item["id"],
                "title": title,
                "description": snippet.get("description", ""),
                "published_at": snippet.get("publishedAt", ""),
                "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                "tags": "|".join(snippet.get("tags", [])),
                "category_id": snippet.get("categoryId", ""),
                "live_broadcast_content": snippet.get("liveBroadcastContent", ""),
                "duration_iso": content.get("duration", ""),
                "duration_sec": duration_sec,
                "caption": content.get("caption", "false"),
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0)),
                "favorite_count": int(stats.get("favoriteCount", 0)),
                # 分析補助フィールド
                "is_shorts": is_shorts(duration_sec),
                "weekday": _weekday(snippet.get("publishedAt", "")),
                "title_length": len(title),
                "description_length": len(snippet.get("description", "")),
                "tag_count": len(snippet.get("tags", [])),
                "fetched_at": fetched_at,
            })

    print(f"[取得] 動画詳細: {len(details)} 件")
    return details


def _weekday(published_at: str) -> str:
    """ISO 8601 の日時文字列から曜日名（日本語）を返す。"""
    weekdays_ja = ["月", "火", "水", "木", "金", "土", "日"]
    try:
        dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        return weekdays_ja[dt.weekday()]
    except Exception:
        return ""


# ─────────────────────────────────────────
# コメントの取得
# ─────────────────────────────────────────

def fetch_comments(
    youtube, video_ids: list[str], max_per_video: int = 100
) -> list[dict]:
    """各動画のトップレベルコメントを取得する。"""
    all_comments: list[dict] = []
    fetched_at = now_jst()

    for video_id in video_ids:
        try:
            next_page_token = None
            collected = 0

            while collected < max_per_video:
                response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(100, max_per_video - collected),
                    pageToken=next_page_token,
                    textFormat="plainText",
                ).execute()

                for item in response.get("items", []):
                    top = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
                    all_comments.append({
                        "comment_thread_id": item["id"],
                        "video_id": video_id,
                        "text": top.get("textOriginal", ""),
                        "author": top.get("authorDisplayName", ""),
                        "like_count": int(top.get("likeCount", 0)),
                        "reply_count": int(item.get("snippet", {}).get("totalReplyCount", 0)),
                        "published_at": top.get("publishedAt", ""),
                        "fetched_at": fetched_at,
                    })
                    collected += 1

                next_page_token = response.get("nextPageToken")
                if not next_page_token or collected >= max_per_video:
                    break

        except HttpError as e:
            # コメント無効動画（403）やプライベート・削除済み動画（404）をスキップ
            if e.resp.status == 403:
                print(f"[スキップ] コメント取得不可 (403): video_id={video_id} detail={e.error_details}")
            elif e.resp.status == 404:
                print(f"[スキップ] 動画が見つかりません (404): video_id={video_id}")
            else:
                raise

    print(f"[取得] コメント: {len(all_comments)} 件")
    return all_comments


# ─────────────────────────────────────────
# メイン処理
# ─────────────────────────────────────────

def main() -> None:
    if not API_KEY:
        raise EnvironmentError(
            "環境変数 YOUTUBE_API_KEY が設定されていません。\n"
            ".env ファイルに YOUTUBE_API_KEY=<あなたのAPIキー> を記載してください。"
        )
    if not CHANNEL_ID:
        raise EnvironmentError(
            "環境変数 YOUTUBE_CHANNEL_ID が設定されていません。\n"
            ".env ファイルに YOUTUBE_CHANNEL_ID=<チャンネルID> を記載してください。"
        )

    youtube = build("youtube", "v3", developerKey=API_KEY)

    # 1. チャンネル情報
    print("=== チャンネル情報を取得します ===")
    channel_info = fetch_channel_info(youtube, CHANNEL_ID)
    save_json(channel_info, OUTPUT_DIR / "channel_info.json")

    # 2. 動画 ID リスト
    print("=== 動画 ID リストを取得します ===")
    uploads_playlist_id = channel_info["uploads_playlist_id"]
    video_ids = fetch_video_ids(youtube, uploads_playlist_id)

    # 3. 動画詳細
    print("=== 動画詳細を取得します ===")
    videos = fetch_video_details(youtube, video_ids)
    save_json(videos, OUTPUT_DIR / "videos.json")
    save_csv(videos, OUTPUT_DIR / "videos.csv")

    # 4. コメント
    print("=== コメントを取得します ===")
    comments = fetch_comments(youtube, video_ids, MAX_COMMENTS_PER_VIDEO)
    save_json(comments, OUTPUT_DIR / "comments.json")
    save_csv(comments, OUTPUT_DIR / "comments.csv")

    print("\n✅ データ取得完了。`data/` フォルダを確認してください。")
    print(f"   チャンネル: {channel_info['title']} （{channel_info['video_count']} 本）")
    print(f"   取得動画数: {len(videos)}")
    print(f"   取得コメント数: {len(comments)}")


if __name__ == "__main__":
    main()
