from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios_pedidos, name='menu_pedidos'),
    path('pedido/<int:pedido_id>/confirmado/', views.pedido_confirmado, name='pedido_confirmado'),
    path('modificar-pagina/', views.panel_modificar_pagina, name='modificar_pagina'),
]
