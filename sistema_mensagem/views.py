from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Dono, Especie, Pet, Vacina, Vacinacao
from .forms import DonoForm, EspecieForm, PetForm, VacinaForm, VacinacaoForm, VacinacaoUpdateForm
from django.core.management import call_command
from sistema_mensagem.management.commands.send_reminder import enviar_lembretes_atrasados


# ─────────────────────────────────────────────
# Autenticação (sem @login_required)
# ─────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'sistema_mensagem/login.html', {'erro': True})

    return render(request, 'sistema_mensagem/login.html')


# ─────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────

@login_required
def dashboard(request):
    hoje = timezone.localdate()
    amanha = hoje + timedelta(days=1)

    vacinas_hoje = Vacinacao.objects.filter(data_proxima=hoje, vacinado=False)
    vacinas_amanha = Vacinacao.objects.filter(data_proxima=amanha, vacinado=False)
    vacinas_atrasadas = Vacinacao.objects.filter(data_proxima__lt=hoje, vacinado=False)

    context = {
        'hoje': vacinas_hoje,
        'amanha': vacinas_amanha,
        'atrasadas': vacinas_atrasadas
    }

    return render(request, 'sistema_mensagem/dashboard.html', context)


# ─────────────────────────────────────────────
# Lembretes
# ─────────────────────────────────────────────

@login_required
def enviar_lembretes(request):
    if request.method == 'POST':
        call_command('send_reminder')
    return redirect('dashboard')

@login_required
def enviar_lembretes_atrasados(request, id):
    hoje = timezone.localdate()
    atrasadas = Vacinacao.objects.filter(data_proxima__lt=hoje, vacinado=False)
    
    if request.method == 'POST':
        ids_selecionados = request.POST.getlist('vacinacoes')  # lista de ids marcados
        vacinacoes = Vacinacao.objects.filter(id__in=ids_selecionados)
        
        enviar_lembretes_atrasados(vacinacoes)

        return ('dashboard')

    return render(request, 'sistema_mensagem/lembretes_atrasados.html', {
        'atrasadas': atrasadas,
    })          


# ─────────────────────────────────────────────
# Cadastro
# ─────────────────────────────────────────────

@login_required
def cadastro_home(request):
    return render(request, 'sistema_mensagem/cadastro_home.html')

@login_required
def cadastrar_dono(request):
    form = DonoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Dono'})

@login_required
def cadastrar_especie(request):
    form = EspecieForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Espécie'})

@login_required
def cadastrar_pet(request):
    form = PetForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Pet'})

@login_required
def cadastrar_vacina(request):
    form = VacinaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Vacina'})

@login_required
def cadastrar_vacinacao(request):
    form = VacinacaoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastro_home')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': 'Cadastrar Vacinação'})


# ─────────────────────────────────────────────
# Listagem
# ─────────────────────────────────────────────

@login_required
def listagem_home(request):
    return render(request, 'sistema_mensagem/listagem_home.html')

@login_required
def listar_donos(request):
    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': Dono.objects.all(),
        'titulo': '👤 Lista de Donos',
    })

@login_required
def listar_especies(request):
    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': Especie.objects.all(),
        'titulo': '🐾 Lista de Espécies',
    })

@login_required
def listar_pets(request):
    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': Pet.objects.select_related('dono', 'especie'),
        'titulo': '🐶 Lista de Pets',
    })

@login_required
def listar_vacinas(request):
    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': Vacina.objects.all(),
        'titulo': '💉 Lista de Vacinas',
    })

@login_required
def listar_vacinacoes(request):
    return render(request, 'sistema_mensagem/listar.html', {
        'objetos': Vacinacao.objects.all(),
        'titulo': '📅 Lista de Vacinações',
    })


# ─────────────────────────────────────────────
# Detalhes
# ─────────────────────────────────────────────

@login_required
def detalhar_dono(request, id):
    dono = get_object_or_404(Dono, id=id)
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

@login_required
def detalhar_especie(request, id):
    especie = get_object_or_404(Especie, id=id)
    campos = [
        ('Nome', especie.nome),
        ('Emojis', especie.emojis),
    ]
    return render(request, 'sistema_mensagem/detalhe.html', {
        'titulo': f'Especie: {especie.nome}',
        'campos': campos,
    })

@login_required
def detalhar_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    campos = [
        ('Nome', pet.nome),
        ('Espécie', pet.especie.nome),
        ('Dono', pet.dono.nome),
    ]
    return render(request, 'sistema_mensagem/detalhe.html', {
        'titulo': f'Pet: {pet.nome}',
        'campos': campos,
    })

@login_required
def detalhar_vacina(request, id):
    vacina = get_object_or_404(Vacina, id=id)
    campos = [
        ('Nome', vacina.nome),
        ('Periodicidade (dias)', vacina.periodicidade_dias),
    ]
    return render(request, 'sistema_mensagem/detalhe.html', {
        'titulo': f'Vacina: {vacina.nome}',
        'campos': campos,
    })

@login_required
def detalhar_vacinacao(request, id):
    vacinacao = get_object_or_404(Vacinacao, id=id)
    campos = [
        ('Pet', vacinacao.pet.nome),
        ('Dono', vacinacao.pet.dono.nome),
        ('Vacina', vacinacao.vacina.nome),
        ('Vacinado', 'Sim' if vacinacao.vacinado else 'Não'),
        ('Data de Aplicação', vacinacao.data_aplicada.strftime('%d/%m/%Y')),
        ('Data Próxima', vacinacao.data_proxima.strftime('%d/%m/%Y') if vacinacao.data_proxima else 'N/A'),
        ('Notificado 1 dia antes', 'Sim' if vacinacao.notificado_1_dia else 'Não'),
        ('Data Notificação 1 dia antes', vacinacao.data_notificacao_1_dia.strftime('%d/%m/%Y %H:%M') if vacinacao.data_notificacao_1_dia else 'N/A'),
        ('Notificado 3 dias antes', 'Sim' if vacinacao.notificado_3_dias else 'Não'),
        ('Data Notificação 3 dias antes', vacinacao.data_notificacao_3_dias.strftime('%d/%m/%Y %H:%M') if vacinacao.data_notificacao_3_dias else 'N/A'),
    ]
    return render(request, 'sistema_mensagem/detalhe.html', {
        'titulo': f'Vacinação: {vacinacao.pet.nome} - {vacinacao.vacina.nome}',
        'campos': campos,
    })


# ─────────────────────────────────────────────
# Edição
# ─────────────────────────────────────────────

@login_required
def editar_dono(request, id):
    dono = get_object_or_404(Dono, id=id)
    form = DonoForm(request.POST or None, instance=dono)
    if form.is_valid():
        form.save()
        return redirect('listar_donos')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': f'✏️ Editar Dono: {dono.nome}'})

@login_required
def editar_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    form = PetForm(request.POST or None, instance=pet)
    if form.is_valid():
        form.save()
        return redirect('listar_pets')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': f'✏️ Editar Pet: {pet.nome}'})

@login_required
def editar_especie(request, id):
    especie = get_object_or_404(Especie, id=id)
    form = EspecieForm(request.POST or None, instance=especie)
    if form.is_valid():
        form.save()
        return redirect('listar_especies')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': f'✏️ Editar Espécie: {especie.nome}'})

@login_required
def editar_vacina(request, id):
    vacina = get_object_or_404(Vacina, id=id)
    form = VacinaForm(request.POST or None, instance=vacina)
    if form.is_valid():
        form.save()
        return redirect('listar_vacinas')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': f'✏️ Editar Vacina: {vacina.nome}'})

@login_required
def editar_vacinacao(request, id):
    vacinacao = get_object_or_404(Vacinacao, id=id)
    form = VacinacaoUpdateForm(request.POST or None, instance=vacinacao)
    if form.is_valid():
        form.save()
        return redirect('listar_vacinacoes')
    return render(request, 'sistema_mensagem/form.html', {'form': form, 'titulo': f'✏️ Editar Vacinação: {vacinacao.pet.nome} - {vacinacao.vacina.nome}'})


# ─────────────────────────────────────────────
# Exclusão
# ─────────────────────────────────────────────

@login_required
def deletar_dono(request, id):
    dono = get_object_or_404(Dono, id=id)
    if request.method == 'POST':
        dono.delete()
        return redirect('listar_donos')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {'objeto': dono, 'titulo': f'Confirmar exclusão: {dono.nome}'})

@login_required
def deletar_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    if request.method == 'POST':
        pet.delete()
        return redirect('listar_pets')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {'objeto': pet, 'titulo': f'Confirmar exclusão: {pet.nome}'})

@login_required
def deletar_especie(request, id):
    especie = get_object_or_404(Especie, id=id)
    if request.method == 'POST':
        especie.delete()
        return redirect('listar_especies')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {'objeto': especie, 'titulo': f'Confirmar exclusão: {especie.nome}'})

@login_required
def deletar_vacina(request, id):
    vacina = get_object_or_404(Vacina, id=id)
    if request.method == 'POST':
        vacina.delete()
        return redirect('listar_vacinas')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {'objeto': vacina, 'titulo': f'Confirmar exclusão: {vacina.nome}'})

@login_required
def deletar_vacinacao(request, id):
    vacinacao = get_object_or_404(Vacinacao, id=id)
    if request.method == 'POST':
        vacinacao.delete()
        return redirect('listar_vacinacoes')
    return render(request, 'sistema_mensagem/confirmar_delecao.html', {'objeto': vacinacao, 'titulo': f'Confirmar exclusão: {vacinacao.pet.nome} - {vacinacao.vacina.nome}'})