from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    
    path('cadastro/', cadastro_home, name='cadastro_home'),
    path('cadastro/dono/', cadastrar_dono, name='cadastrar_dono'),
    path('cadastro/especie/', cadastrar_especie, name='cadastrar_especie'),
    path('cadastro/pet/', cadastrar_pet, name='cadastrar_pet'),
    path('cadastro/vacina/', cadastrar_vacina, name='cadastrar_vacina'),
    path('cadastro/vacinacao/', cadastrar_vacinacao, name='cadastrar_vacinacao'),
]