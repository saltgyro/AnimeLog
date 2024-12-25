from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import (TemplateView,CreateView,FormView,View)
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm,RegistForm,UserLoginForm,CustomUserCreationForm,UserEditForm,forms
from django.urls import reverse_lazy
from .models import (Anime,Genres,Seasons,Studios,Tags,User_anime_relations)
from django.db.models import F
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

class UserLoginView(FormView):
    template_name = 'html/user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('anime_tracker:index')
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        remember = form.cleaned_data['remember']
        user = authenticate(email=email,password=password)
        if user:
            login(self.request,user)
            if remember:
                self.request.session.set_expiry(120000)  # 秒間保持
            else:
                self.request.session.set_expiry(0)  # ブラウザが閉じられると終了
        return super().form_valid(form)

class UserLogoutView(View):
    def get(self,request,*args, **kwargs):
        return render(request,'user_logout.html')
    
    def post(self,request,*args, **kwargs):
        logout(request)
        return redirect('anime_tracker:index')

class RegistUseView(CreateView):
    template_name = 'html/regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('anime:index')
    
# 最初に呼びされる。ビュー
def index(request):
    # デフォルトの並び順
    sort_option = request.GET.get('sort', 'season-desc')  # デフォルトはシーズン新しい順
    print("取得したsort_optionの値:", sort_option)
    # クエリセットのベース
    animes = Anime.objects.annotate(
        seasons__year=F('anime_seasons__season_id__year'),
        seasons__season=F('anime_seasons__season_id__season')
    )

    # 並び順の分岐
    if sort_option == 'average_rating':  # 人気順
        print("選択されたソートオプション: 人気順")
        animes = animes.order_by('-average_rating')
    elif sort_option == 'season':  # シーズン古い順
        print("選択されたソートオプション: シーズン古い順")
        animes = animes.order_by('seasons__year', 'seasons__season')
    elif sort_option == 'season-desc':  # シーズン新しい順
        print("選択されたソートオプション: シーズン新しい順")
        animes = animes.order_by('-seasons__year', '-seasons__season')
    elif sort_option == 'watched_count':  # 登録数順
        print("選択されたソートオプション: 登録数順")
        animes = animes.order_by('-watched_count')
    else:  # デフォルト: シーズン新しい順
        print("デフォルトのソートオプションが適用されました")
        animes = animes.order_by('-seasons__year', '-seasons__season')
    
    # その他のデータを取得
    genres = Genres.objects.all()
    tags = Tags.objects.all()
    studios = Studios.objects.all()
    seasons = Seasons.objects.all()

    return render(request, 'html/index.html', {
        'animes': animes,
        'genres': genres,
        'tags': tags,
        'studios': studios,
        'seasons': seasons
    })

def regist_view(request):
    user_form = CustomUserCreationForm(request.POST or None)  
    
    # フォームの状態をコンソールに表示
    print("フォームのデータ:", user_form.data)  # POSTデータが渡されているか確認
    print("フォームのバリデーション:", user_form.is_valid())  # True or False
    print("フォームのエラー:", user_form.errors)  # バリデーションエラーの詳細
    
    
    
    if user_form.is_valid():
        user_form.save()
        return redirect('anime_tracker:user_login')  # 登録成功後にログイン画面へリダイレクト

    return render(request, 'html/regist.html', context={
        'user_form': user_form,
    })
    
@login_required
def user_edit(request):
    user_edit_form = forms.UserEditForm(request.POST or None,isinstance=request.user)
    if user_edit_form.is_valid():
        user_edit_form.save()
        messages.success(request,'更新完了しました')
    return render(request,'anime/user_edit.html',context={
        'user_edit_form':user_edit_form
    })
@login_required
def user_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, user=request.user, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールが更新されました。')
            
            return render(request, 'html/user_edit.html', {'form': form})# アカウント設定画面のまま
    else:
        form = UserEditForm(user=request.user, instance=request.user)
    return render(request, 'html/user_edit.html', {'form': form})


    
@login_required
def change_password(request):
    pass


#パスワードリセット
def request_password_reset(request):
    pass


#アニメ詳細画面
def animeDetailView(request, pk):
    anime = get_object_or_404(Anime, pk=pk) 
    return render(request, 'html/anime_detail.html', {'anime': anime})


#アニメ詳細画面で追加
@login_required
def update_status(request):
    print('update_statusが呼び出された')
    if request.method == "POST":
        # 生のリクエストボディを出力
        print("リクエストボディ:", request.body)
        try:
            # JSONデータを読み取る
            data = json.loads(request.body)  # リクエストボディをJSONとして解析
            anime_id = data.get('anime_id')  # JSONからアニメIDを取得
            status = data.get('status')      # JSONからステータスを取得

            print(f"アニメID: {anime_id}")
            print(f"ステータス: {status}")
            
            # anime_id = request.POST.get('anime_id')
            # print(f"アニメID: {anime_id}")
            # status = request.POST.get('status')
            # print(f"ステータス: {status}")
            anime = get_object_or_404(Anime, id=anime_id)
            user = request.user
            print(f"リクエストユーザー: {user.nickname}")
            # デバッグ用の出力

            # ユーザーとアニメの関係を更新
            relation, created = User_anime_relations.objects.get_or_create(user_id=user, anime_id=anime)

            # ステータス更新処理
            if status == "watched":
                relation.is_watched = True
                relation.is_favorite = False  # 視聴済にした場合、お気に入りをリセット
                relation.is_plan_to_watch = False
            elif status == "favorite":
                if relation.is_watched:  # 視聴済のみお気に入りに設定可能
                    relation.is_favorite = True
            elif status == "plan_to_watch":
                relation.is_plan_to_watch = True
                relation.is_watched = False
                relation.is_favorite = False

            relation.save()

            # JSONレスポンスの内容
            return JsonResponse({
                "is_watched": relation.is_watched,
                "is_favorite": relation.is_favorite,
                "is_plan_to_watch": relation.is_plan_to_watch,
            })

        except Exception as e:
            print(f"Anime の取得でエラー: {e}")
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=400)


#アニメ視聴管理更新
def animeDetailView(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    user_relation = None
    if request.user.is_authenticated:
        user_relation = User_anime_relations.objects.filter(user_id=request.user, anime_id=anime).first()
    return render(request, 'html/anime_detail.html', {'anime': anime, 'user_relation': user_relation})

#ユーザー評価入力
def update_rating(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            anime_id = data.get('anime_id')
            rating = data.get('rating')

            if not 0.0 <= rating <= 5.0:
                return JsonResponse({"error": "Invalid rating value."}, status=400)

            anime = get_object_or_404(Anime, id=anime_id)
            user = request.user
            relation, created = User_anime_relations.objects.get_or_create(user_id=user, anime_id=anime)
            relation.rating = rating
            relation.save()
            
            print("relation更新"+ str(relation.rating))
            # アニメの平均評価を更新


            return JsonResponse({"message": "Rating updated successfully.", "average_rating": anime.average_rating})
            # return JsonResponse({"message": "Rating updated successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

def search_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # リクエストボディをJSONで読み込み
        
        animes = Anime.objects.all()

        if 'genre' in data:
            animes = animes.filter(genres__id__in=data['genre'])  # ジャンルに基づく検索
        if 'tag' in data:
            animes = animes.filter(tags__id__in=data['tag'])      # タグに基づく検索
        if 'season' in data:
            animes = animes.filter(seasons__id__in=data['season']) # シーズンに基づく検索
        if 'studio' in data:
            animes = animes.filter(studios__id__in=data['studio']) # 制作スタジオに基づく検索

        # 重複を排除
        animes = animes.distinct()

        # JSON形式で結果を返す
        results = [
            {
                'id': anime.id,
                'title': anime.title,
                'thumbnail': anime.thumbnail.url if anime.thumbnail else '',
            } for anime in animes
        ]
        # JSON形式で結果を返す
        results = [
            {
                'id': anime.id,
                'title': anime.title,
                'thumbnail': anime.thumbnail.url if anime.thumbnail else '',
            } for anime in animes
        ]
        return JsonResponse({'results': results})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

#視聴済/お気に入り/視聴予定に応じたビュー
def anime_list_view(request, status):
    """ステータスに応じたアニメリストを表示"""
    user = request.user  # 現在のログインユーザー
    if not user.is_authenticated:
        return redirect('anime_tracker:user_login')  # ログインしていない場合はリダイレクト

    # ステータスに基づいてフィルタリング
    if status == "watched":
        relations = User_anime_relations.objects.filter(user_id=user, is_watched=True)
    elif status == "favorite":
        relations = User_anime_relations.objects.filter(user_id=user, is_favorite=True)
    elif status == "plan_to_watch":
        relations = User_anime_relations.objects.filter(user_id=user, is_plan_to_watch=True)
    else:
        relations = User_anime_relations.objects.none()  # 空のクエリセット

    # 関連するアニメを取得
    animes = [relation.anime_id for relation in relations]

    return render(request, 'html/anime_list.html', {'animes': animes, 'status': status})
