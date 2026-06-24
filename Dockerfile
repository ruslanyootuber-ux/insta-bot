FROM python:3.12-slim

# Kerakli tizim kutubxonalarini o'rnatish
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kutubxonalarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodni nusxalash
COPY . .

# Botni ishga tushirish
CMD ["python", "main.py"]
