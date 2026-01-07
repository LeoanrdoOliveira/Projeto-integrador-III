# pacientes/urls.py
from django.urls import path, include
from rest_framework import routers
from . import views

# Router da API
router = routers.DefaultRouter()
router.register(r'pacientes', views.PacienteViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro_paciente, name='cadastro_paciente'),
    path('lista/', views.lista_pacientes, name='lista_pacientes'),
    path('receita/', views.gerar_receita, name='gerar_receita'),
    path('remover/<int:paciente_id>/', views.remover_paciente, name='remover_paciente'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Endpoints da API
    path('api/', include(router.urls)),
]
