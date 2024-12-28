from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,PermissionsMixin)
from django.urls import reverse_lazy
from django.core.validators import MinValueValidator, MaxValueValidator


class UserManager(BaseUserManager):
    def create_user(self,email,password):
        if not email:
            raise ValueError('メールアドレスは必須です')
        if not password:
            raise ValueError('パスワードを入力してください')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email, password,nickname):
        user = self.model(
            email=email,
            password=password,
            nickname=nickname
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
    
class Users(AbstractBaseUser,PermissionsMixin):
    nickname = models.CharField(max_length=128)
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)  # 管理画面用
    is_staff = models.BooleanField(default=False)  # 管理画面用
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
    
    objects = UserManager()
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.nickname
    
    def get_absolute_url(self):
        return reverse_lazy('home')
    
class Series(models.Model):#シリーズテーブル
    title = models.CharField(max_length=255)#シリーズ名
    
    def __str__(self):
        return self.title  # シリーズ名を返す  

    
class Character(models.Model):  # アニメのキャラクターモデル
    name = models.CharField(max_length=255)  # キャラクター名
    anime_id = models.ForeignKey('Anime', on_delete=models.SET_NULL, related_name='characters_set', null=True)  # アニメとの関連
    voice_actor = models.CharField(max_length=255)  # 声優

    def __str__(self):
        return self.name

class Song(models.Model):
    SONG_CHOICES = [
        (0, 'OP'),      # 0がオープニング
        (1, 'ED'),      # 1がエンディング
        (2, 'Insert'),  # 2が挿入歌
    ]
    title = models.CharField(max_length=255)  # 曲名
    song_type = models.IntegerField(choices=SONG_CHOICES, default=0) # 曲のタイプ
    artists = models.CharField(max_length=255, null=True, blank=True) #アーティスト名
    note = models.CharField(max_length=255, null=True, blank=True)  # エピソード範囲や使用の詳細を記録

    def __str__(self):
        return self.title

class Anime(models.Model):
    series_id = models.ForeignKey(Series, on_delete=models.SET_NULL, related_name='animes', null=True, blank=True)#シリーズID
    title = models.CharField(max_length=128)#タイトル名
    synopsis = models.TextField(null=True, blank=True)#シナリオ
    start_date = models.DateField(null=True, blank=True)#放送開始日
    end_date = models.DateField(null=True, blank=True)#放送終了日
    episode_count = models.IntegerField(default=0)#総話数
    thumbnail = models.FileField(upload_to='thumbnails/', null=True, blank=True)  # サムネイル画像ファイル
    average_rating = models.FloatField(null=True, blank=True, default=0.0)#平均評価
    watched_count = models.IntegerField(null=True, blank=True, default=0)#登録者数
    favorite_count = models.IntegerField(null=True, blank=True, default=0)#お気に入りの数
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    characters = models.ManyToManyField('Character', related_name='animes')#キャラクター
    songs = models.ManyToManyField('Song', related_name='animes')#曲
    
    genres = models.ManyToManyField(
        'Genres',
        through='Anime_genres',
        related_name='animes'
    )#Genresとの多対多の関係
    
    seasons = models.ManyToManyField(
        'Seasons',
        through='Anime_seasons',
        related_name='animes'
    )#Seasonsとの多対多の関係
    
    studios = models.ManyToManyField(
        'Studios',
        through='Anime_studio',
        related_name='animes'
    )#Studiosとの多対多の関係
    
    tags = models.ManyToManyField(
        'Tags',
        through='Anime_tags',
        related_name='animes'
    )#Tagsとの多対多の関係
    
    def __str__(self):
        return self.title

class User_anime_relations(models.Model):#ユーザーのアニメの視聴管理
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_anime_relations', null=True, blank=True)
    anime_id = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='user_anime_relations', null=True, blank=True)
    is_watched = models.BooleanField(default=False)#視聴済か
    is_favorite = models.BooleanField(default=False)#お気に入りか
    is_plan_to_watch = models.BooleanField(default=False)#視聴予定か
    rating = models.FloatField(default=0.0,
    validators=[
        MinValueValidator(0.0),  # 最小値 0.0
        MaxValueValidator(5.0)   # 最大値 5.0
    ])#ユーザー評価
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    def __str__(self):
        return f"{self.user_id.nickname if self.user_id else '未設定'} - {self.anime_id.title if self.anime_id else '未設定'}"

    def save(self, *args, **kwargs):
        # 通常の保存処理を実行
        super().save(*args, **kwargs)

        # 平均評価を再計算
        if self.anime_id:
            self.update_anime_average_rating()
            self.update_anime_watched_count()

    def update_anime_average_rating(self):
        """アニメの平均評価を再計算して保存する"""
        related_ratings = User_anime_relations.objects.filter(anime_id=self.anime_id).values_list('rating', flat=True)
        average_rating = sum(related_ratings) / len(related_ratings) if related_ratings else 0.0
        self.anime_id.average_rating = average_rating
        print(f"平均評価が更新されました: {average_rating}")
        self.anime_id.save()

    def update_anime_watched_count(self):
        """視聴済みのカウントを更新して保存する"""
        watched_count = User_anime_relations.objects.filter(anime_id=self.anime_id, is_watched=True).count()
        self.anime_id.watched_count = watched_count
        print(f"視聴済みカウントが更新されました: {watched_count}")
        self.anime_id.save()


class Seasons(models.Model):#(放送シーズン)
    SEASON_CHOICES = [
        (0, '冬'),  # 0が冬
        (1, '春'),  # 1が春
        (2, '夏'),  # 2が夏
        (3, '秋'),  # 3が秋
    ]
    
    year = models.IntegerField()#放送年
    season = models.IntegerField(choices=SEASON_CHOICES)#放送季節
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    def __str__(self):
        return f"{self.year} - {self.get_season_display()}"

class Anime_seasons(models.Model):#(アニメ-シーズン中間テーブル)
    anime_id = models.ForeignKey(Anime, on_delete=models.SET_NULL, related_name='anime_seasons', null=True, blank=True)
    season_id = models.ForeignKey(Seasons, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    def __str__(self):
        return f"{self.anime_id.title} - {self.season_id}"
    
class Studios(models.Model):#(制作スタジオ)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    def __str__(self):
        return self.name
    
class Anime_studio(models.Model):#(アニメ-制作スタジオ中間テーブル)
    anime_id = models.ForeignKey(Anime, on_delete=models.SET_NULL, related_name='anime_studio', null=True, blank=True)
    studio_id = models.ForeignKey(Studios, on_delete=models.SET_NULL, related_name='anime_studio', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    def __str__(self):
        return f"{self.anime.title} - {self.studio.name}"
    
class Genres(models.Model):#(ジャンル一覧)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    def __str__(self):
        return self.name

class Anime_genres(models.Model):#(アニメ-ジャンル中間テーブル)
    anime_id = models.ForeignKey(Anime, on_delete=models.SET_NULL, related_name='anime_genres', null=True, blank=True)
    genre_id = models.ForeignKey(Genres, on_delete=models.SET_NULL, related_name='anime_genres', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    def __str__(self):
        return f"{self.anime_id.title} - {self.genre_id.name}"
    
class Tags(models.Model):#(タグ一覧)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    def __str__(self):
        return self.name
    
class Anime_tags(models.Model):#(アニメ-タグ中間テーブル)
    anime_id = models.ForeignKey(Anime, on_delete=models.SET_NULL, related_name='anime_tags', null=True, blank=True)
    tag_id = models.ForeignKey(Tags, on_delete=models.SET_NULL, related_name='anime_tags', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)#登録日時
    updated_at = models.DateTimeField(auto_now=True)#更新日時
    
    def __str__(self):
        anime_title = self.anime_id.title if self.anime_id else "Unknown Anime"
        tag_name = self.tag_id.name if self.tag_id else "Unknown Tag"
        return f"{anime_title} - {tag_name}"




