import os
import django
import requests
import sys

print('実行ディレクトリ:', os.getcwd())

# プロジェクトのルートディレクトリを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# モデルを絶対パスでインポート
from anime_tracker.models import Anime

print(f"現在のパス: {os.getcwd()}")  # カレントディレクトリを出力
print(f"sys.path: {sys.path}")  # Pythonの検索パスを出力

# Djangoの設定をロード
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnimeLog.AnimeLog.settings')
print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")  # 確認用

django.setup()

# Annict APIのURLとアクセストークン
API_URL = "https://api.annict.com/graphql"
ACCESS_TOKEN = "QBsj4vOUWkqM4IjJTEm-ZzUkQKPc2C9JSXUnxd4wwnY"

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
}

query = """
query {
    searchWorks(orderBy: { field: SEASON, direction: DESC }, first: 10) {
        nodes {
            id
            title
            synopsis
            startDate
            endDate
            episodesCount
            image {
                url
            }
        }
    }
}
"""

try:
    response = requests.post(API_URL, headers=headers, json={"query": query})

    print(f"HTTPステータスコード: {response.status_code}")
    if response.status_code == 200:
        data = response.json().get("data", {}).get("searchWorks", {}).get("nodes", [])
        print(f"取得データ数: {len(data)}")  # デバッグ用
        for anime_data in data:
            title = anime_data.get("title", "No Title")
            synopsis = anime_data.get("synopsis", "")
            start_date = anime_data.get("startDate", None)
            end_date = anime_data.get("endDate", None)
            episode_count = anime_data.get("episodesCount", 0)
            thumbnail_url = anime_data.get("image", {}).get("url", None)

            # 既存データのチェック（タイトルが一致するもの）
            anime, created = Anime.objects.get_or_create(
                title=title,
                defaults={
                    "synopsis": synopsis,
                    "start_date": start_date,
                    "end_date": end_date,
                    "episode_count": episode_count,
                }
            )

            if created:
                print(f"新しいアニメを作成: {title}")
            else:
                print(f"既存のアニメをスキップ: {title}")
    else:
        print(f"APIリクエストが失敗しました: {response.status_code}")
        print(response.json())
except Exception as e:
    print(f"エラーが発生しました: {e}")
