from django.urls import path
from .views import *

urlpatterns = [
    # Dashboard
    path('', dashboard, name='dashboard'),
    
    # Páginas de cadastro
    path('cadastro/', cadastro_home, name='cadastro_home'),
    path('cadastro/dono/', cadastrar_dono, name='cadastrar_dono'),
    path('cadastro/especie/', cadastrar_especie, name='cadastrar_especie'),
    path('cadastro/pet/', cadastrar_pet, name='cadastrar_pet'),
    path('cadastro/vacina/', cadastrar_vacina, name='cadastrar_vacina'),
    path('cadastro/vacinacao/', cadastrar_vacinacao, name='cadastrar_vacinacao'),
    
    # Páginas de listagem
    path('listagem/', listagem_home, name='listagem_home'),
    path('listagem/donos/', listar_donos, name='listar_donos'),
    path('listagem/especies/', listar_especies, name='listar_especies'),
    path('listagem/pets/', listar_pets, name='listar_pets'),
    path('listagem/vacinas/', listar_vacinas, name='listar_vacinas'),
    path('listagem/vacinacoes/', listar_vacinacoes, name='listar_vacinacoes'),
]