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
        
        atrasadas = Vacinacao.objects.filter(
            data_proxima__lt=hoje,
            vacinado=False
        )
        
        if not vacinas_1_dia.exists() and not vacinas_3_dias.exists():
            print("Nenhum lembrete.")
            return
        
        enviar_lembretes(vacinas_1_dia, 1)
        enviar_lembretes(vacinas_3_dias, 3)
 
def enviar_lembretes(vacinas_para_enviar, dias_para_vencimento):
    
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_TOKEN")
    from_whatsapp = os.getenv("TWILIO_WHATSAPP")

    client = Client(account_sid, auth_token)
        
    for v in vacinas_para_enviar:
        try:
            mensagem = f"""
🐾 Olá, {v.pet.dono.nome}! Aqui é do petshop Cantinho Cão e Gato.

A vacina do *{v.pet.nome}* {v.pet.especie.emojis} vence em {v.data_proxima.strftime('%d/%m')} 💉

Para manter a saúde dele(a) em dia 🐶🐈, recomendamos agendar a próxima dose.

> Esse número não responde mensagens, Fale com {os.getenv('NUMERO_SUPORTE')} para marcar!
"""

            numero = f"whatsapp:+55{v.pet.dono.telefone}"
            client.messages.create(
                body=mensagem,
                from_=from_whatsapp,
                to=numero
            )

            if dias_para_vencimento == 1:
                v.notificado_1_dia = True
                v.data_notificacao_1_dia = timezone.now()
            elif dias_para_vencimento == 3:
                v.notificado_3_dias = True
                v.data_notificacao_3_dias = timezone.now()

            v.save()
            
            if dias_para_vencimento == 1:
                print(f"Mensagem enviada para {numero} as {v.data_notificacao_1_dia} sobre o pet {v.pet.nome} com vacina vencendo em {v.data_proxima.strftime('%d/%m')}")

            elif dias_para_vencimento == 3:
                print(f"Mensagem enviada para {numero} as {v.data_notificacao_3_dias} sobre o pet {v.pet.nome} com vacina vencendo em {v.data_proxima.strftime('%d/%m')}")

        except Exception as e:
            print(f"Erro ao enviar para {numero} as {timezone.now()}: {e}")
                
def enviar_lembretes_atrasados(vacinas_atrasadas):
    
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_TOKEN")
    from_whatsapp = os.getenv("TWILIO_WHATSAPP")
    
    client = Client(account_sid, auth_token)
    
    for v in vacinas_atrasadas:
        try:
            mensagem = f"""
🐾 Olá, {v.pet.dono.nome}! Aqui é do petshop Cantinho Cão e Gato.

A vacina do *{v.pet.nome}* {v.pet.especie.emojis} venceu em {v.data_proxima.strftime('%d/%m')} 💉

Para manter a saúde dele(a) em dia 🐶🐈, recomendamos agendar a próxima dose.

> Esse número não responde mensagens, Fale com {os.getenv('NUMERO_SUPORTE')} para marcar!
"""
            numero = f"whatsapp:+55{v.pet.dono.telefone}"
            client.messages.create(
                body=mensagem,
                from_=from_whatsapp,
                to=numero
            )
            
            print(f"Mensagem enviada para {numero} as {timezone.now()} sobre o pet {v.pet.nome} com vacina vencendo em {v.data_proxima.strftime('%d/%m')}")

        except Exception as e:
            print(f"Erro ao enviar para {numero} as {timezone.now()}: {e}")