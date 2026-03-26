from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Vacinacao
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