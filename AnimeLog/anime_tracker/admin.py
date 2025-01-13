from django.contrib import admin
from .models import (
    Anime, Genres, Tags, Seasons, Studios, Series, User_anime_relations,
    Anime_genres, Anime_seasons, Anime_studio, Anime_tags, Song, Character, Artist, VoiceActor
)

# Genre モデルの管理
@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    search_fields = ['name']  # nameフィールドを検索可能にする

# Tag モデルの管理
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    search_fields = ['name']  # nameフィールドを検索可能にする

# Season モデルの管理
@admin.register(Seasons)
class SeasonsAdmin(admin.ModelAdmin):
    search_fields = ['year', 'season']  # yearとseasonを検索可能にする

# Studio モデルの管理
@admin.register(Studios)
class StudiosAdmin(admin.ModelAdmin):
    search_fields = ['name']  # nameフィールドを検索可能にする

# Series モデルの管理
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

# SongAdminの設定
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'song_type', 'get_artist_name')  # アーティスト名を表示するメソッドを追加
    
    def get_artist_name(self, obj):
        return obj.artist.name if obj.artist else "なし"  # Artistの名前を表示
    get_artist_name.short_description = 'アーティスト'  # 列名をカスタマイズ

admin.site.register(Song, SongAdmin)
admin.site.register(Artist)

# Characterモデルの設定
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_voice_actor']  # 表示したいフィールドを設定
    search_fields = ['name', 'anime__title', 'voice_actor__name']  # 検索できるフィールドを設定
    
    def get_voice_actor(self, obj):
        return obj.voice_actor.name if obj.voice_actor else "なし"  # 声優名を表示
    get_voice_actor.short_description = '声優'

# VoiceActor モデルの管理
@admin.register(VoiceActor)
class VoiceActorAdmin(admin.ModelAdmin):
    search_fields = ['name']  # voice_actorの名前を検索可能にする

# Characterインラインで表示
class CharacterInline(admin.TabularInline):
    model = Character
    extra = 1
    autocomplete_fields = ['voice_actor']  # 声優を選択できるようにする

# Songインラインで表示
class SongInline(admin.TabularInline):
    model = Anime.songs.through  # ManyToManyの中間テーブルを指定
    extra = 1
    
# Anime-Studio中間テーブル用インライン
class AnimeStudioInline(admin.TabularInline):
    model = Anime_studio  # AnimeとStudioの中間テーブルを指定
    extra = 1
    autocomplete_fields = ['studio_id']  # studio_idを指定

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    inlines = [AnimeGenresInline, AnimeTagsInline, AnimeSeasonsInline, CharacterInline, SongInline, AnimeStudioInline]  # インライン表示

    # 一覧表示で表示するフィールド
    list_display = ['title', 'start_date', 'end_date', 'episode_count', 'initial']
    
    # 検索対象のフィールド
    search_fields = ['title', 'manual_keyword']
    
    # フィルタリング対象のフィールド
    list_filter = ['start_date', 'end_date']
    
    # 読み取り専用フィールド
    readonly_fields = ['average_rating', 'watched_count', 'favorite_count']
    
    # 管理画面で編集可能なフィールド（ManyToManyFieldを除外）
    fields = [
        'sort_key',
        'series_id',
        'title', 
        'title_kana',
        'synopsis', 
        'start_date', 
        'end_date', 
        'episode_count', 
        'thumbnail', 
        'characters',  # ManyToManyFieldではないのでそのまま使える
        'songs',       # 同上
        'manual_keyword',  # 手動キーワードフィールド
        'initial',
    ]
