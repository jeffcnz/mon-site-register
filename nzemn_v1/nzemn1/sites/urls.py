from django.urls import path

from . import views

urlpatterns = [
    # ex: /sites/
    path('', views.index, name='index'),
    # ex: /sites/id/5/
    path('id/<int:site_id>/', views.site, name='site'),
]
