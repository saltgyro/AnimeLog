from django.urls import path
from .import views
from .views import(index,RegistUseView,UserLoginView,UserLogoutView,animeDetailView,update_status,CustomPasswordResetView,CustomPasswordResetDoneView,CustomPasswordResetCompleteView,CustomPasswordResetConfirmView)
from django.contrib.auth import views as auth_views

app_name = 'anime_tracker'


urlpatterns = [
    path('',views.index,name='index'),
    path('home/', views.home, name='home'),
    path('regist/', views.regist_view, name='regist'), 
    
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),# パスワードリセット用のURLパターン
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),# リセットリクエスト送信後に表示するページ
    
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),# リセット用URL（ユーザーとトークンを含む）
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),# パスワードリセット完了後に表示されるページ
    
    
    path('user_login/',UserLoginView.as_view(),name='user_login'),#ページへ遷移
    path('user_logout/',UserLogoutView.as_view(),name='user_logout'),#ページへ遷移
    path('edit/', views.user_edit, name='user_edit'),#ページへ遷移
    
    path('<int:pk>/', views.animeDetailView, name='anime_detail'),  # 詳細ページ
    path('update_status/', views.update_status, name='update_status'), 
    path('update_rating/', views.update_rating, name='update_rating'),
    path('search/', views.search_view, name='search'),  # 検索用URL
    
    path('toggle-tag/', views.toggle_tag, name='toggle_tag'), # タグ更新URL
]
