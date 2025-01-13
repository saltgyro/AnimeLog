from django.core.management.base import BaseCommand
import requests
from anime_tracker.models import Anime
import os
from pathlib import Path
from django.conf import settings
from datetime import datetime

def parse_date(date_str):
    """
    日付形式をパースする関数。
    無効な形式の場合はNoneを返す。
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    except ValueError:
        print(f"無効な日付形式: {date_str}")
        return None

def save_thumbnail(anime, thumbnail_url):
    """
    サムネイル画像を保存する関数。
    """
    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            thumbnails_dir = os.path.join(settings.MEDIA_ROOT, "thumbnails")
            Path(thumbnails_dir).mkdir(parents=True, exist_ok=True)
            file_name = os.path.join(thumbnails_dir, f"{anime.id}.jpg")
            with open(file_name, "wb") as f:
                f.write(response.content)
            anime.thumbnail.name = f"thumbnails/{anime.id}.jpg"
            anime.save()
            print(f"サムネイル保存完了: {file_name}")
        else:
            print(f"サムネイル取得失敗: {thumbnail_url}")
    except Exception as e:
        print(f"サムネイル保存中にエラー: {e}")

class Command(BaseCommand):
    help = "Annict APIからアニメデータをインポートします"

    def handle(self, *args, **kwargs):
        print("Annict APIからデータを取得開始...")

        # APIトークンの取得
        ACCESS_TOKEN = "QBsj4vOUWkqM4IjJTEm-ZzUkQKPc2C9JSXUnxd4wwnY"
        if not ACCESS_TOKEN:
            print("APIトークンが設定されていません。settings.pyにANNICT_ACCESS_TOKENを追加してください。")
            return

        API_URL = "https://api.annict.com/v1/works"

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
        }

        params = {
            "per_page": 10,
            "sort_season": "desc",
        }

        response = requests.get(API_URL, headers=headers, params=params)
        print(f"APIリクエストステータスコード: {response.status_code}")

        if response.status_code == 200:
            works = response.json().get("works", [])
            print(f"{len(works)}件のデータを取得")

            for work in works:
                title = work.get("title", "No Title")
                synopsis = work.get("synopsis", "")
                released_on = work.get("released_on") or work.get("released_on_about") or None
                start_date = parse_date(released_on)
                episode_count = work.get("episodes_count", 0)
                thumbnail_url = work.get("images", {}).get("recommended_url") or work.get("images", {}).get("facebook", {}).get("og_image_url")

                # 保存予定データを確認
                print(f"保存予定データ: タイトル={title}, 開始日={start_date}, サムネイルURL={thumbnail_url}")

                if not title:
                    print("タイトルが存在しないデータをスキップ")
                    continue

                anime, created = Anime.objects.get_or_create(
                    title=title,
                    defaults={
                        "synopsis": synopsis,
                        "start_date": start_date,
                        "episode_count": episode_count,
                    },
                )

                if created:
                    print(f"新しいアニメを作成: {title}")
                    if thumbnail_url:
                        save_thumbnail(anime, thumbnail_url)
                else:
                    print(f"既存のアニメをスキップ: {title}")
        else:
            print(f"APIリクエスト失敗: {response.status_code} - {response.text}")
