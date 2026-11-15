FROM python:3.9-alpine

WORKDIR /app

# Сначала копируем только требования и устанавливаем их (для кэширования)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]