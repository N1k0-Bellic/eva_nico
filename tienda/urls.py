from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('juego/<int:juego_id>/', views.detalle_juego, name='detalle'),
]