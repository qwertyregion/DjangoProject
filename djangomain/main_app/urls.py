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
from django.urls import path, include
from sait_app.views import list_notfound, eror_403
from django.conf.urls import handler404, handler403
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from users_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sait_app.urls', namespace='sait_app')),
    path('users/', include(('users_app.urls', 'users_app'), namespace='users_app')),
    path('__debug__/', include(debug_toolbar.urls)),

    # path('accounts/', include('django.contrib.auth.urls')),
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    # path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# + debug_toolbar_urls()
#
handler404 = list_notfound
handler403 = eror_403
