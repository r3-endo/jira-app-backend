"""jira_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# URLパターンとビューのマッチング情報などを保持したモジュール
# 実際のURLパターンをapi直下のurls.pyに移譲している
# import
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # api直下のurls.pyを参照
    path('api/', include('api.urls')),
    # jwtトークンを返却。認証サイトに移動
    path('authen/', include('djoser.urls.jwt')),
]
# project直下のmediaフォルダとmediaのURLを紐付ける
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
