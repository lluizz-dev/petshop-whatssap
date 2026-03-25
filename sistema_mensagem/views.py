from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Vacinacao

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