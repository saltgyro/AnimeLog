from django.core.management.base import BaseCommand
from anime_tracker.models import Genres, Tags, Seasons

# 実行の際
# python manage.py create_initial_data

class Command(BaseCommand):
    help = 'ジャンル、タグ、シーズンの初期データを作成'

    def handle(self, *args, **kwargs):
        # ジャンルのデータ
        genres = [
            "SF/ファンタジー", "ロボット/メカ", "アクション/バトル", "コメディ/ギャグ",
            "恋愛/ラブコメ", "日常/ほのぼの", "スポーツ/競技", "ホラー/サスペンス/推理",
            "歴史/戦記", "戦争/ミリタリー", "ドラマ／青春", "ショート"
        ]
        for genre in genres:
            Genres.objects.get_or_create(name=genre)
        self.stdout.write(self.style.SUCCESS('ジャンルを登録しました'))

        # タグのデータ
        tags = [
            "泣ける", "心温まる", "家族愛", "鬱展開", "暇つぶし", "神作画", "悲劇的結末",
            "どんでん返し", "笑える", "衝撃的な展開", "タイムリープ", "異世界転生", "復讐",
            "デスゲーム", "成長物語", "音楽が魅力的"
        ]
        for tag in tags:
            Tags.objects.get_or_create(name=tag)
        self.stdout.write(self.style.SUCCESS('タグを登録しました'))

        # シーズンのデータ
        SEASONS = [
            (0, '冬'), (1, '春'), (2, '夏'), (3, '秋')
        ]
        for year in range(2003, 2025):  # 2003年から2024年まで
            for season_value, season_name in SEASONS:
                Seasons.objects.get_or_create(year=year, season=season_value)
        self.stdout.write(self.style.SUCCESS('シーズンを登録しました'))
