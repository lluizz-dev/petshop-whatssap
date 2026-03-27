from urllib import request

from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Dono, Especie, Pet, Vacina, Vacinacao
from .forms import DonoForm, EspecieForm, PetForm, VacinaForm, VacinacaoForm

# Create your views here.

def dashboard(request):
    hoje = timezone.localdate()
    amanha = hoje + timedelta(days=1)

    vacinas_amanha = Vacinacao.objects.filter(data_proxima=amanha, notificado=False)
    vacinas_atrasadas = Vacinacao.objects.filter(data_proxima__lt=hoje, notificado=False)

    context = {
        'amanha': vacinas_amanha,
        'atrasadas': vacinas_atrasadas
    }

    return render(request, 'sistema_mensagem/dashboard.html', context)

def cadastro_home(request):
    return render(request, 'sistema_mensagem/cadastro_home.html')

def cadastrar_dono(request):
    form = DonoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Dono'})

def cadastrar_especie(request):
    form = EspecieForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Espécie'})


def cadastrar_pet(request):
    form = PetForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Pet'})


def cadastrar_vacina(request):
    form = VacinaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Vacina'})


def cadastrar_vacinacao(request):
    form = VacinacaoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Vacinação'})

def listagem_home(request):
    return render(request, 'sistema_mensagem/listagem_home.html')

def listar_donos(request):
    donos = Dono.objects.all()

    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': donos,
        'titulo': '👤 Lista de Donos'
    })

def listar_especies(request):
    especies = Especie.objects.all()

    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': especies,
        'titulo': '🐾 Lista de Espécies'
    })

def listar_pets(request):
    pets = Pet.objects.select_related('dono', 'especie')

    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': pets,
        'titulo': '🐶 Lista de Pets'
    })

def listar_vacinas(request):
    vacinas = Vacina.objects.all()
    
    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': vacinas,
        'titulo': '💉 Lista de Vacinas'
    })

def listar_vacinacoes(request):
    vacinacoes = Vacinacao.objects.all()
    
    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': vacinacoes,
        'titulo': '📅 Lista de Vacinações'
    })
    
def detalhar_dono(request, id):
    dono = get_object_or_404(Dono, id=id)
    # Criar lista de campos para exibir
    campos = [
        ('Nome', dono.nome),
        ('Telefone', dono.telefone),
        ('Email', dono.email),
        ('Ativo', dono.ativo),
        ('Criado em', dono.criado_em.strftime('%d/%m/%Y %H:%M')),
    ]
    return render(request, 'sistema_mensagem/detalhe.html', {
        'titulo': f'Dono: {dono.nome}',
        'campos': campos,
    })
    
def detalhar_especie(request, id):
    especie = get_object_or_404(Especie, id=id)
    # Criar lista de campos para exibir
    campos = [
        ('Nome', especie.nome),
        ('Emojis', especie.emojis),
    ]
    return render(request, 'sistema_mensagem/detalhe.html', {
        'titulo': f'Especie: {especie.nome}',
        'campos': campos,
    })
    
def detalhar_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    # Criar lista de campos para exibir
    campos = [
        ('Nome', pet.nome),
        ('Espécie', pet.especie.nome),
        ('Dono', pet.dono.nome),
    ]
    return render(request, 'sistema_mensagem/detalhe.html', {
        'titulo': f'Pet: {pet.nome}',
        'campos': campos,
    })
    
def detalhar_vacina(request, id):
    vacina = get_object_or_404(Vacina, id=id)
    # Criar lista de campos para exibir
    campos = [
        ('Nome', vacina.nome),
        ('Periodicidade (dias)', vacina.periodicidade_dias),
    ]
    return render(request, 'sistema_mensagem/detalhe.html', {
        'titulo': f'Vacina: {vacina.nome}',
        'campos': campos,
    })

def detalhar_vacinacao(request, id):
    vacinacao = get_object_or_404(Vacinacao, id=id)
    # Criar lista de campos para exibir
    campos = [
        ('Pet', vacinacao.pet.nome),
        ('Dono', vacinacao.pet.dono.nome),
        ('Vacina', vacinacao.vacina.nome),
        ('Data de Aplicação', vacinacao.data_aplicada.strftime('%d/%m/%Y')),
        ('Data Próxima', vacinacao.data_proxima.strftime('%d/%m/%Y') if vacinacao.data_proxima else 'N/A'),
        ('Notificado', 'Sim' if vacinacao.notificado else 'Não'),
        ('Data Notificação', vacinacao.data_notificacao.strftime('%d/%m/%Y %H:%M') if vacinacao.data_notificacao else 'N/A'),
        
    ]
    return render(request, 'sistema_mensagem/detalhe.html', {
        'titulo': f'Vacinação: {vacinacao.pet.nome} - {vacinacao.vacina.nome}',
        'campos': campos,
    })

def editar_home(request):
    return render(request, 'sistema_mensagem/editar_home.html')


def excluir_home(request):
    return render(request, 'sistema_mensagem/excluir_home.html')