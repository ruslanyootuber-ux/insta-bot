FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install instagrapi requests
CMD ["python", "main.py"]
