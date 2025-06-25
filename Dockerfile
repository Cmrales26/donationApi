FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Instala las dependencias necesarias del sistema
RUN apt-get update && \
    apt-get install -y gcc && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get autoremove -y && \
    apt-get clean

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
