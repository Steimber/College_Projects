from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_lista, name='lista'),
    path('categoria/<int:categoria_id>/', views.blog_por_categoria, name='categoria'),
]
