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
        
        

        account_sid = os.getenv("TWILIO_SID")
        auth_token = os.getenv("TWILIO_TOKEN")
        from_whatsapp = os.getenv("TWILIO_WHATSAPP")

        client = Client(account_sid, auth_token)
        
        vacinas_1_dia = Vacinacao.objects.filter(
            data_proxima=amanha,
            notificado_1_dia=False,
            vacinado=False
        )

        vacinas_3_dias = Vacinacao.objects.filter(
            data_proxima=tres_dias,
            notificado_3_dias=False,
            vacinado=False
        )
        
        if not vacinas_1_dia.exists() and not vacinas_3_dias.exists():
            print("Nenhum lembrete.")
            return

        for v in vacinas_1_dia:
            try:
                mensagem = f"""
🐾 Olá, {v.pet.dono.nome}! Aqui é do petshop Cantinho Cão e Gato.

A vacina do *{v.pet.nome}* {v.pet.especie.emojis} vence em {v.data_proxima.strftime('%d/%m')} 💉

Para manter a saúde dele(a) em dia 🐶🐈, recomendamos agendar a próxima dose.

Fale com {os.getenv('NUMERO_SUPORTE')} para marcar!
"""

                numero = f"whatsapp:+55{v.pet.dono.telefone}"
                client.messages.create(
                    body=mensagem,
                    from_=from_whatsapp,
                    to=numero
                )

                v.notificado_1_dia = True
                v.data_notificacao_1_dia = timezone.now()
                v.save()

                print(f"Mensagem enviada para {numero} as {v.data_notificacao_1_dia} sobre o pet {v.pet.nome} com vacina vencendo em {v.data_proxima.strftime('%d/%m')}")

            except Exception as e:
                print(f"Erro ao enviar para {numero} as {timezone.now()}: {e}")
                
        for v in vacinas_3_dias:
            try:
                mensagem = f"""
🐾 Olá, {v.pet.dono.nome}! Aqui é do petshop Cantinho Cão e Gato.

A vacina do *{v.pet.nome}* {v.pet.especie.emojis} vence em {v.data_proxima.strftime('%d/%m')} 💉

Para manter a saúde dele(a) em dia 🐶🐈, recomendamos agendar a próxima dose.

Fale com {os.getenv('NUMERO_SUPORTE')} para marcar!
"""

                numero = f"whatsapp:+55{v.pet.dono.telefone}"
                
                client.messages.create(
                    body=mensagem,
                    from_=from_whatsapp,
                    to=numero
                )

                v.notificado_3_dias = True
                v.data_notificacao_3_dias = timezone.now()
                v.save()

                print(f"Mensagem enviada para {numero} as {v.data_notificacao_3_dias} sobre o pet {v.pet.nome} com vacina vencendo em {v.data_proxima.strftime('%d/%m')}")

            except Exception as e:
                print(f"Erro ao enviar para {numero} as {timezone.now()}: {e}")