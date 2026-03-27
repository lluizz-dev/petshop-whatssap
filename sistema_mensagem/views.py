from django.shortcuts import render, redirect
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

def editar_home(request):
    return render(request, 'sistema_mensagem/editar_home.html')


def excluir_home(request):
    return render(request, 'sistema_mensagem/excluir_home.html')