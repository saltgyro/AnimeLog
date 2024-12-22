from django.urls import path
from .import views
from .views import(UserLoginView,UserLogoutView,)

app_name = 'anime_tracker'


urlpatterns = [
    path('',views.index,name='index'),
    path('regist/', views.regist_view, name='regist'), 
    path('user_login/',UserLoginView.as_view(),name='user_login'),#ページへ遷移
    path('user_logout/',UserLogoutView.as_view(),name='user_logout'),#ページへ遷移
]
