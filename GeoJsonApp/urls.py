"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from MapApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.map, name="map"),
    path('upload/', views.upload_file, name='upload'),
    path('download_point/<int:point_id>', views.download_point, name='download_point'),
    path('download_line/<int:line_id>', views.download_line, name='download_line'),
    path('download_poly/<int:poly_id>', views.download_poly, name='download_poly'),
    path('download_mpoly/<int:mpoly_id>', views.download_multipoly, name='download_mpoly'),

]
