import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from sistema_mensagem.models import Vacinacao
from twilio.rest import Client

load_dotenv()

class Command(BaseCommand):
    help = 'Envia lembretes de vacinação'

    def handle(self, *args, **kwargs):
        hoje = timezone.localdate()
        amanha = hoje + timedelta(days=1)

        account_sid = os.getenv("TWILIO_SID")
        auth_token = os.getenv("TWILIO_TOKEN")
        from_whatsapp = os.getenv("TWILIO_WHATSAPP")

        client = Client(account_sid, auth_token)

        vacinas = Vacinacao.objects.filter(
            data_proxima__lte=amanha,
            lembrete_enviado=False
        )

        if not vacinas:
            print("Nenhum lembrete.")
            return

        for v in vacinas:
            numero = f"whatsapp:+55{v.pet.dono.telefone}"

            mensagem = f"""
Olá {v.pet.dono.nome}! 👋

O pet {v.pet.nome} 🐶 precisa tomar a vacina {v.vacina.nome} 💉

Procure a clínica para manter tudo em dia!
"""

            try:
                client.messages.create(
                    body=mensagem,
                    from_=from_whatsapp,
                    to=numero
                )

                v.lembrete_enviado = True
                v.save()

                print(f"Mensagem enviada para {numero}")

            except Exception as e:
                print(f"Erro ao enviar para {numero}: {e}")