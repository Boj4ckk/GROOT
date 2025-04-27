FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    streamlink \
    libgl1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    libjpeg-dev \
    zlib1g-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install debugpy

EXPOSE 5000
EXPOSE 5678

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "run.py"]