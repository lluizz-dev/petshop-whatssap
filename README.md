# 🐾 PetShop — Sistema de Lembretes de Vacinação

Sistema web desenvolvido em Django para gerenciar vacinas de pets e enviar lembretes automáticos via WhatsApp usando a API do Twilio.

---

## ✨ Funcionalidades

- Dashboard com vacinas do dia, amanhã e atrasadas
- Cadastro de donos, pets, espécies, vacinas e vacinações
- Envio automático de lembretes via WhatsApp (Twilio)
- Sistema de login para proteger o acesso
- CRUD completo de todas as entidades

---

## 🛠️ Tecnologias

- Python 3.13+
- Django 5.2
- PostgreSQL
- Twilio (WhatsApp API)

---

## 📦 Pré-requisitos

### Python

Antes de começar, você precisa ter o Python instalado na sua máquina:

- 🔗 [Download Python (python.org)](https://www.python.org/downloads/) — página oficial de download
- 📖 [Guia de instalação oficial](https://docs.python.org/3/installing/index.html) — documentação detalhada por sistema operacional

> **Versão recomendada:** Python 3.13 ou superior.

### PostgreSQL

Este projeto usa PostgreSQL como banco de dados. Você precisa tê-lo instalado e rodando:

- 🔗 [Download PostgreSQL](https://www.postgresql.org/download/) — página oficial de download
- 📖 [Documentação oficial](https://www.postgresql.org/docs/current/index.html) — guia completo de instalação e uso

> Após instalar, crie um banco de dados e um usuário para o projeto, e preencha as variáveis correspondentes no `.env`.

### Twilio (serviço pago)

O envio de mensagens via WhatsApp é feito através do **Twilio**, uma plataforma externa de comunicação. Para utilizá-lo você precisa criar uma conta e contratar o serviço — há custos por mensagem enviada.

- 🔗 [Criar conta no Twilio](https://www.twilio.com/try-twilio)
- 📖 [Documentação da API WhatsApp](https://www.twilio.com/docs/whatsapp/api) — referência completa da API
- 📖 [Quickstart — enviar sua primeira mensagem](https://www.twilio.com/docs/whatsapp/quickstart) — passo a passo para configurar e testar

> Após criar sua conta, acesse o [Console do Twilio](https://console.twilio.com/) para obter o `ACCOUNT_SID` e o `AUTH_TOKEN`.

---

## 🐳 Recomendação: usar Docker (opcional mas recomendado)

O projeto já inclui um `docker-compose.yml` pronto. Se você tiver o Docker instalado, pode subir o banco de dados com um único comando, sem precisar instalar o PostgreSQL manualmente.

- 🔗 [Instalar Docker](https://docs.docker.com/get-docker/)

Para subir apenas o banco de dados:

```bash
docker compose up -d
```

Para subir tudo (banco + aplicação):

```bash
docker compose up --build
```

> **Atenção:** com Docker, o `POSTGRES_HOST` no seu `.env` deve ser `postgres` (nome do serviço definido no `docker-compose.yml`), não `localhost`.

---

## ⚙️ Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua-secret-key-aqui

DEBUG=True

POSTGRES_DB=nome_do_banco
POSTGRES_USER=usuario_do_banco
POSTGRES_PASSWORD=senha_do_banco
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

> Para gerar uma nova `SECRET_KEY`:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Crie um superusuário para acessar o sistema

```bash
python manage.py createsuperuser
```

### 7. Rode o servidor

```bash
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)

---

## 📁 Estrutura do projeto

```
petshop/
├── petshop/                  # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sistema_mensagem/         # App principal
│   ├── management/commands/  # Comando de envio de lembretes
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── .env                      # Não versionado
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 📲 Envio de lembretes via WhatsApp

O sistema envia lembretes automaticamente para os donos de pets com vacinas próximas. O comando pode ser rodado manualmente ou agendado com `cron`:

```bash
python manage.py send_reminder
```

Para agendar no Linux (todo dia às 8h):
```bash
0 8 * * * /caminho/para/venv/bin/python /caminho/do/projeto/manage.py send_reminder
```

---

## 🔒 Variáveis de ambiente necessárias

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | `True` para desenvolvimento, `False` para produção |
| `POSTGRES_DB` | Nome do banco de dados |
| `POSTGRES_USER` | Usuário do PostgreSQL |
| `POSTGRES_PASSWORD` | Senha do PostgreSQL |
| `POSTGRES_HOST` | Host do banco (ex: `localhost`) |
| `POSTGRES_PORT` | Porta do banco (padrão: `5432`) |
| `TWILIO_ACCOUNT_SID` | SID da conta Twilio |
| `TWILIO_AUTH_TOKEN` | Token de autenticação Twilio |
| `TWILIO_WHATSAPP_FROM` | Número Twilio no formato `whatsapp:+14155238886` |

---

## 📽️ Vídeo Demonstrativo

Confira o sistema em funcionamento no LinkedIn:

[![Assistir demonstração](https://img.shields.io/badge/LinkedIn-Assistir%20demonstração-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/posts/lluizz-dev_python-django-whatsapp-activity-7447623019994320896-V2cd?utm_source=share&utm_medium=member_desktop&rcm=ACoAAF2wZiQB_zbGxdvvzaK1n9gmzch6qWPBxkk)

---

## 📝 Licença

Este projeto foi desenvolvido para uso interno de um petshop. Todos os direitos reservados.
