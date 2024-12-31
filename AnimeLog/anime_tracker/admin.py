from django.contrib import admin
from .models import (Anime, Genres, Tags, Seasons, Studios,Series,User_anime_relations,Anime_genres,Anime_seasons,Anime_studio,Anime_tags,Song,Character)

@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    search_fields = ['name']  # nameフィールドを検索可能にする

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    search_fields = ['name']  # nameフィールドを検索可能にする

@admin.register(Seasons)
class SeasonsAdmin(admin.ModelAdmin):
    search_fields = ['year', 'season']  # yearとseasonを検索可能にする

@admin.register(Studios)
class StudiosAdmin(admin.ModelAdmin):
    search_fields = ['name']  # nameフィールドを検索可能にする

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    search_fields = ['title']  # titleフィールドを検索可能にする

# Anime-Genres中間テーブル用インライン
class AnimeGenresInline(admin.TabularInline):
    model = Anime_genres
    extra = 1
    autocomplete_fields = ['genre_id']

# Anime-Tags中間テーブル用インライン
class AnimeTagsInline(admin.TabularInline):
    model = Anime_tags
    extra = 1
    autocomplete_fields = ['tag_id']

# Anime-Seasons中間テーブル用インライン
class AnimeSeasonsInline(admin.TabularInline):
    model = Anime_seasons
    extra = 1
    autocomplete_fields = ['season_id']

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'song_type', 'artists', 'note']  # 表示したいフィールドを設定
    list_filter = ['song_type']  # 曲のタイプ（OP, ED, 挿入歌）でフィルタリング


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'voice_actor']  # 表示したいフィールドを設定
    search_fields = ['name', 'anime__title', 'voice_actor']  # 検索できるフィールドを設定
    

# Characterモデル用インライン表示
class CharacterInline(admin.TabularInline):
    model = Character
    extra = 1
    
class SongInline(admin.TabularInline):
    model = Anime.songs.through  # ManyToManyの中間テーブルを指定
    extra = 1
    
# Animeモデル用Adminクラス
@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    inlines = [AnimeGenresInline, AnimeTagsInline, AnimeSeasonsInline, CharacterInline, SongInline]  # キャラクターと曲をインラインで表示
    # inlines = [AnimeGenresInline, AnimeTagsInline, AnimeSeasonsInline]
    list_display = ['title', 'start_date', 'end_date', 'episode_count']
    search_fields = ['title']
    list_filter = ['start_date', 'end_date']
    readonly_fields = ['average_rating', 'watched_count', 'favorite_count']  # 編集禁止のフィールド
    