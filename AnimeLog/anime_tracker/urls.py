from django.urls import path
from .import views
from .views import(index,RegistUseView,UserLoginView,UserLogoutView,animeDetailView,update_status)
from django.contrib.auth import views as auth_views

app_name = 'anime_tracker'


urlpatterns = [
    path('',views.index,name='index'),
    path('home/', views.home, name='home'),
    path('regist/', views.regist_view, name='regist'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),# パスワードリセット用のURLパターン
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),# リセットリクエスト送信後に表示するページ
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),# リセット用URL（ユーザーとトークンを含む）
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),# パスワードリセット完了後に表示されるページ
    
    
    path('user_login/',UserLoginView.as_view(),name='user_login'),#ページへ遷移
    path('user_logout/',UserLogoutView.as_view(),name='user_logout'),#ページへ遷移
    path('edit/', views.user_edit, name='user_edit'),#ページへ遷移
    
    path('<int:pk>/', views.animeDetailView, name='anime_detail'),  # 詳細ページ
    path('update_status/', views.update_status, name='update_status'), 
    path('update_rating/', views.update_rating, name='update_rating'),
    path('search/', views.search_view, name='search'),  # 検索用URL
    
    
]
