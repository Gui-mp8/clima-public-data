# Use an official Python runtime as the base image
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget \
    unzip \

WORKDIR /app
EXPOSE 8000

COPY . .

ENV PORT=8000
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]
# CMD ["python", "api/main.py"]