FROM python:3.9

# Defina o fuso horário para America/Sao_Paulo
RUN ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Copie o código da sua aplicação para o contêiner
COPY . .

# Configurar variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Executar comandos para criar o superusuário Django
RUN python manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Executar migrações adicionais (se necessário)
RUN python manage.py migrate

# Configurar gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
