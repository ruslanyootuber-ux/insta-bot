FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Loglarni real vaqtda ko'rish uchun -u parametrini qo'shdik
CMD ["python", "-u", "main.py"]
