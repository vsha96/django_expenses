"""edusite URL Configuration

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
from django.urls import path, include

from expenses import views_oauth


from expenses.admin import admin_reports





urlpatterns = [
    path('expenses/', include('expenses.urls')),
    path("basic-admin/", admin.site.urls),
    path("admin/", admin_reports.urls),
    # path("admin/", admin.site.urls),
    path('', include('social_django.urls', namespace='social')), 

    # oath
    path('accounts/profile/', views_oauth.create_account_oauth, name='create_account_oauth'),
]

