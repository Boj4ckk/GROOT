FROM laudio/pyodbc:latest 

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

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir debugpy


COPY . .

EXPOSE 5000 5678

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "run.py"]