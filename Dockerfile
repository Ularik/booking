FROM python:3.14.2-slim

# Настройка окружения: не писать .pyc, не буферизовать логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# 1. Устанавливаем инструменты
RUN apt-get update && apt-get install -y curl gnupg2

# 3. Установка драйверов и зависимостей
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Создаем директории и пользователя (безопасность)
RUN mkdir -p /usr/www/logs && \
    useradd -m -d /usr/www ular && \
    chown -R ular:ular /usr/www

WORKDIR /usr/www/

# Сначала ставим зависимости (используем кэш, пока requirements.txt не изменится)
COPY --chown=ular:ular req.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r req.txt

# Копируем приложение
COPY --chown=ular:ular src ./src

# Переключаемся на пользователя
USER ular

# Запуск через uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]