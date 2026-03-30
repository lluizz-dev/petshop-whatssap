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
        tres_dias = hoje + timedelta(days=3)
        
        mensagem = f"""
🐾 Olá, {v.pet.dono.nome}! Aqui é do petshop Cantinho Cão e Gato.

A vacina *{v.vacina.nome}* do {v.pet.nome} vence em {v.data_proxima.strftime('%d/%m')} 💉

Para manter a saúde dele(a) em dia 🐶🐈, recomendamos agendar a próxima dose.

Fale com a gente para marcar!
"""

        numero = f"whatsapp:+55{v.pet.dono.telefone}"

        account_sid = os.getenv("TWILIO_SID")
        auth_token = os.getenv("TWILIO_TOKEN")
        from_whatsapp = os.getenv("TWILIO_WHATSAPP")

        client = Client(account_sid, auth_token)

        vacinas_1_dia = Vacinacao.objects.filter(
            data_proxima__lte=amanha,
            notificado=False
        )

        vacinas_3_dias = Vacinacao.objects.filter(
            data_proxima__lte=tres_dias,
            notificado=False
        )
        
        if not vacinas_1_dia and not vacinas_3_dias:
            print("Nenhum lembrete.")
            return

        for v in vacinas_1_dia:
            try:
                client.messages.create(
                    body=mensagem,
                    from_=from_whatsapp,
                    to=numero
                )

                v.notificado = True
                v.data_notificacao = timezone.now()
                v.save()

                print(f"Mensagem enviada para {numero} as {v.data_notificacao}")

            except Exception as e:
                print(f"Erro ao enviar para {numero} as {timezone.now()}: {e}")
                
        for v in vacinas_3_dias:
            try:
                client.messages.create(
                    body=mensagem,
                    from_=from_whatsapp,
                    to=numero
                )

                v.notificado = True
                v.data_notificacao = timezone.now()
                v.save()

                print(f"Mensagem enviada para {numero} as {v.data_notificacao}")

            except Exception as e:
                print(f"Erro ao enviar para {numero} as {timezone.now()}: {e}")