from django.urls import path
from .import views
from .views import(RegistUseView,UserLoginView,UserLogoutView,animeDetailView,update_status)

app_name = 'anime_tracker'


urlpatterns = [
    path('',views.index,name='index'),
    path('regist/', views.regist_view, name='regist'), 
    path('user_login/',UserLoginView.as_view(),name='user_login'),#ページへ遷移
    path('user_logout/',UserLogoutView.as_view(),name='user_logout'),#ページへ遷移
    path('regist/', views.regist_view, name='regist'), 
    path('edit/', views.user_edit, name='user_edit'),#ページへ遷移
    path('change_password/',views.change_password,name='change_password'),#ページへ遷移
    
    path('<int:pk>/', views.animeDetailView, name='anime_detail'),  # 詳細ページ
    path('update_status/', views.update_status, name='update_status'), 
    path('update_rating/', views.update_rating, name='update_rating'),
    path('search/', views.search_view, name='search'),  # 検索用URL
    path('anime_list/<str:status>/', views.anime_list_view, name='anime_list'),
]
