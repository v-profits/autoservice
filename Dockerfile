# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app


# Создать папку под базу
RUN mkdir -p /app/data && chmod -R 777 /app/data

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 5000
EXPOSE 5000

# Команда запуска приложения
CMD ["python", "app.py"]
