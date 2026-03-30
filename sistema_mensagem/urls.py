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
    # Páginas de detalhes
    path('listagem/donos/<int:id>/', detalhar_dono, name='detalhar_dono'),
    path('listagem/especies/<int:id>/', detalhar_especie, name='detalhar_especie'),
    path('listagem/pets/<int:id>/', detalhar_pet, name='detalhar_pet'),
    path('listagem/vacinas/<int:id>/', detalhar_vacina, name='detalhar_vacina'),
    path('listagem/vacinacoes/<int:id>/', detalhar_vacinacao, name='detalhar_vacinacao'),
    
    # Páginas de edição
    path('listagem/donos/<int:id>/editar/', editar_dono, name='editar_dono'),
    path('listagem/especies/<int:id>/editar/', editar_especie, name='editar_especie'),
    path('listagem/pets/<int:id>/editar/', editar_pet, name='editar_pet'),
    path('listagem/vacinas/<int:id>/editar/', editar_vacina, name='editar_vacina'),
    path('listagem/vacinacoes/<int:id>/editar/', editar_vacinacao, name='editar_vacinacao'),
    
    # Páginas de exclusão
    path('listagem/donos/<int:id>/deletar/', deletar_dono, name='deletar_dono'),
    path('listagem/especies/<int:id>/deletar/', deletar_especie, name='deletar_especie'),
    path('listagem/pets/<int:id>/deletar/', deletar_pet, name='deletar_pet'),
    path('listagem/vacinas/<int:id>/deletar/', deletar_vacina, name='deletar_vacina'),
    path('listagem/vacinacoes/<int:id>/deletar/', deletar_vacinacao, name='deletar_vacinacao'),
]