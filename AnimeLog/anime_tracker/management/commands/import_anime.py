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
    if not date_str:  # 空の場合
        return None
    try:
        # 日付形式をパース
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        # 無効な形式の場合
        return None

# サムネイル画像の保存ディレクトリ
THUMBNAILS_DIR = os.path.join(settings.MEDIA_ROOT, "thumbnails")

# サムネイル保存用ディレクトリを事前に作成
Path(THUMBNAILS_DIR).mkdir(parents=True, exist_ok=True)

class Command(BaseCommand):
    help = "Annict APIからアニメデータをインポートします"

    def handle(self, *args, **kwargs):
        self.stdout.write("Annict APIからデータを取得します...")

        # Annict API設定
        API_URL = "https://api.annict.com/v1/works"
        ACCESS_TOKEN = "QBsj4vOUWkqM4IjJTEm-ZzUkQKPc2C9JSXUnxd4wwnY"

        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
        }

        # APIリクエスト
        params = {
            "per_page": 10,  # 取得件数
            "page": 1,  # ページ番号
            "sort_season": "desc",  # シーズン順（降順）
        }

        response = requests.get(API_URL, headers=headers, params=params)
        if response.status_code == 200:
            self.stdout.write(f"APIリクエストのステータスコード: {response.status_code}")
            data = response.json().get("works", [])

            for work in data:
                print("レスポンスデータ:", work)
                title = work.get("title", "No Title")
                synopsis = work.get("synopsis", "")  # synopsisは未提供の場合が多い
                start_date_raw = work.get("released_on", None)  # 放送開始日
                end_date_raw = None  # end_dateはAPIから取得できない可能性あり
                episode_count = work.get("episodes_count", 0)  # エピソード数
                thumbnail_url = work.get("images", {}).get("recommended_url", None)  # サムネイル画像

                # 日付を変換
                start_date = parse_date(start_date_raw)
                end_date = parse_date(end_date_raw)
                # サムネイルがある場合のみ処理を行う
                if thumbnail_url:
                    anime, created = Anime.objects.get_or_create(
                        title=title,
                        defaults={
                            "synopsis": synopsis,
                            "start_date": start_date,
                            "episode_count": episode_count,
                        }
                    )

                    if created:
                        print(f"新しいアニメを作成: {title}")

                        # サムネイル画像を保存
                        response = requests.get(thumbnail_url)
                        if response.status_code == 200:
                            file_name = f"{THUMBNAILS_DIR}/{anime.id}.jpg"
                            with open(file_name, 'wb') as f:
                                f.write(response.content)
                            anime.thumbnail.name = f"thumbnails/{anime.id}.jpg"
                            anime.save()
                    else:
                        print(f"既存のアニメをスキップ: {title}")
                else:
                    print(f"サムネイルがないためスキップ: {title}")

            
            
            
            # for anime_data in data:
            #     # データ取得
            #     title = anime_data.get("title", "No Title")
            #     synopsis = anime_data.get("synopsis", "")
            #     start_date = anime_data.get("released_on", None) or None  # 空文字列をNoneに変換
            #     end_date = anime_data.get("released_on_about", None) or None  # 空文字列をNoneに変換
            #     episode_count = anime_data.get("episodes_count", 0)
            #     thumbnail_url = anime_data.get("images", {}).get("recommended_url", None)


            #     # データベースに保存
            #     anime, created = Anime.objects.get_or_create(
            #         title=title,
            #         defaults={
            #             "synopsis": synopsis,
            #             "start_date": start_date,
            #             "end_date": end_date,
            #             "episode_count": episode_count,
            #         }
            #     )

            #     if created:
            #         self.stdout.write(f"新しいアニメを作成: {title}")

            #         # サムネイル画像の保存
            #         # if thumbnail_url:
            #         #     thumbnail_response = requests.get(thumbnail_url)
            #         #     if thumbnail_response.status_code == 200:
            #         #         file_name = f"thumbnails/{anime.id}.jpg"
            #         #         with open(file_name, 'wb') as f:
            #         #             f.write(thumbnail_response.content)
            #         #         anime.thumbnail.name = file_name
            #         #         anime.save()
            #         #     else:
            #         #         self.stdout.write(f"サムネイルの取得に失敗しました: {thumbnail_url}")
                    
            #         if thumbnail_url:
            #             print(f"サムネイルURL: {thumbnail_url}")  # デバッグ用に出力
            #             response = requests.get(thumbnail_url)
            #             if response.status_code == 200:
            #                 file_name = f"{THUMBNAILS_DIR}/{anime.id}.jpg"
            #                 with open(file_name, 'wb') as f:
            #                     f.write(response.content)
            #                 anime.thumbnail.name = f"thumbnails/{anime.id}.jpg"
            #                 anime.save()
            #             else:
            #                 print(f"サムネイル画像の取得に失敗しました: {response.status_code}")
            #         else:
            #             print(f"サムネイル未提供: {title}")
                    
            #         # if thumbnail_url:
            #         #     response = requests.get(thumbnail_url)
            #         #     if response.status_code == 200:
            #         #         file_name = f"{THUMBNAILS_DIR}/{anime.id}.jpg"
            #         #         with open(file_name, 'wb') as f:
            #         #             f.write(response.content)
            #         #         anime.thumbnail.name = f"thumbnails/{anime.id}.jpg"  # メディアルートからの相対パスを保存
            #         #         anime.save()
            #         #     else:
            #         #         self.stdout.write(f"サムネイルの取得に失敗しました: {thumbnail_url}")
                    
            #     else:
            #         self.stdout.write(f"既存のアニメをスキップ: {title}")

            self.stdout.write("データベースへの保存が完了しました！")
        else:
            self.stderr.write(f"APIリクエストが失敗しました: {response.status_code}")
            self.stderr.write(response.text)
