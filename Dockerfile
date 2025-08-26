# Dockerfile para petrobras-offshore-wells-anomaly-detection-control-charts
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala dependências
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Exponha a porta para Jupyter/Marimo
EXPOSE 8888

# Comando padrão (ajuste conforme necessário)
CMD ["python3"]
