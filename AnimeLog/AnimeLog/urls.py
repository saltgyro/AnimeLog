from django.contrib import admin
from django.urls import path,include
from . import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('anime_tracker/',include('anime_tracker.urls')),
    path('', include('anime_tracker.urls')),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)