"""fast_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from sait_app import views
from django.conf.urls.static import static
from main_app import settings
from sait_app.views import HomeView, AuthorSlugView, PublisherSlugView, TagSlugView
# RegisterPageView

app_name = 'sait_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home', ),
    path('author/<slug:author_slug>/', AuthorSlugView.as_view(), name='author_slug'),
    path('publisher/<slug:publisher_slug>', PublisherSlugView.as_view(), name='publisher_slug'),
    path('tag/<slug:tag_slug>', TagSlugView.as_view(), name='tag_slug'),
    # path('register_page/', RegisterPageView.as_view(), name='register_page'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news, name='news'),
    path('chat/', views.chat, name='chat'),
    re_path(r'^about/(?P<year>\d{4})/', views.about_repath, name='about_repath'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

