"""mapa_da_informacao_api URL Configuration

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
import debug_toolbar
from contrib.router import HybridRouter
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from map.api import MapHybridRouter, mini_maps

from mapa_da_informacao_api import settings

router = HybridRouter()
router.register_router(MapHybridRouter)

urlpatterns = [
    path('editor/', include('django_summernote.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, 'api'), namespace='api'), name='api-root'),
    path('api/mini_maps', mini_maps, name='mini_maps'),
]

if settings.DEBUG:
    urlpatterns.extend([path('__debug__/', include(debug_toolbar.urls))])
