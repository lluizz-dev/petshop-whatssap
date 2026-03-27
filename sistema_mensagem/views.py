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
        'titulo': '👤 Lista de Donos',
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

def editar_dono(request, id):
    dono = get_object_or_404(Dono, id=id)
    form = DonoForm(request.POST or None, instance=dono)

    if form.is_valid():
        form.save()
        return redirect('listar_donos')

    return render(request, 'sistema_mensagem/form.html', {
        'form': form,
        'titulo': f'✏️ Editar Dono: {dono.nome}'
    })
    
def editar_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    form = PetForm(request.POST or None, instance=pet)

    if form.is_valid():
        form.save()
        return redirect('listar_pets')

    return render(request, 'sistema_mensagem/form.html', {
        'form': form,
        'titulo': f'✏️ Editar Pet: {pet.nome}'
    })
    
def editar_especie(request, id):
    especie = get_object_or_404(Especie, id=id)
    form = EspecieForm(request.POST or None, instance=especie)

    if form.is_valid():
        form.save()
        return redirect('listar_especies')

    return render(request, 'sistema_mensagem/form.html', {
        'form': form,
        'titulo': f'✏️ Editar Espécie: {especie.nome}'
    })
    
def editar_vacina(request, id):
    vacina = get_object_or_404(Vacina, id=id)
    form = VacinaForm(request.POST or None, instance=vacina)

    if form.is_valid():
        form.save()
        return redirect('listar_vacinas')

    return render(request, 'sistema_mensagem/form.html', {
        'form': form,
        'titulo': f'✏️ Editar Vacina: {vacina.nome}'
    })
    
def editar_vacinacao(request, id):
    vacinacao = get_object_or_404(Vacinacao, id=id)
    form = VacinacaoForm(request.POST or None, instance=vacinacao)

    if form.is_valid():
        form.save()
        return redirect('listar_vacinacoes')

    return render(request, 'sistema_mensagem/form.html', {
        'form': form,
        'titulo': f'✏️ Editar Vacinação: {vacinacao.pet.nome} - {vacinacao.vacina.nome}'
    })
    
def deletar_dono(request, id):
    dono = get_object_or_404(Dono, id=id)
    if request.method == 'POST':
        dono.delete()
        return redirect('listar_donos')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {
        'objeto': dono,
        'titulo': f'Confirmar exclusão: {dono.nome}'
    })
    
def deletar_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    if request.method == 'POST':
        pet.delete()
        return redirect('listar_pets')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {
        'objeto': pet,
        'titulo': f'Confirmar exclusão: {pet.nome}'
    })

def deletar_especie(request, id):
    especie = get_object_or_404(Especie, id=id)
    if request.method == 'POST':
        especie.delete()
        return redirect('listar_especies')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {
        'objeto': especie,
        'titulo': f'Confirmar exclusão: {especie.nome}'
    })

def deletar_vacina(request, id):
    vacina = get_object_or_404(Vacina, id=id)
    if request.method == 'POST':
        vacina.delete()
        return redirect('listar_vacinas')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {
        'objeto': vacina,
        'titulo': f'Confirmar exclusão: {vacina.nome}'
    })

def deletar_vacinacao(request, id):
    vacinacao = get_object_or_404(Vacinacao, id=id)
    if request.method == 'POST':
        vacinacao.delete()
        return redirect('listar_vacinacoes')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {
        'objeto': vacinacao,
        'titulo': f'Confirmar exclusão: {vacinacao.pet.nome} - {vacinacao.vacina.nome}'
    })