FROM python:3.11-slim

# Evita a gravação de arquivos .pyc e mantém logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências aproveitando o cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o container
COPY . .

# Expõe a porta padrão utilizada pela aplicação
EXPOSE 8080

# Executa a aplicação com o Uvicorn ouvindo em todas as interfaces
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

