from django.core.management.base import BaseCommand
from datetime import date, timedelta
from sistema_mensagem.models import Vacinacao


class Command(BaseCommand):
    help = 'Envia lembretes de vacinação'

    def handle(self, *args, **kwargs):
        hoje = date.today()
        amanha = hoje + timedelta(days=1)

        vacinas = Vacinacao.objects.filter(data_proxima=amanha)

        if not vacinas:
            print("Nenhum lembrete para amanhã.")
            return

        for v in vacinas:
            print(f"""
🐶 Pet: {v.pet.nome}
💉 Vacina: {v.vacina.nome}
👤 Dono: {v.pet.dono.nome}
📱 Telefone: {v.pet.dono.telefone}
""")