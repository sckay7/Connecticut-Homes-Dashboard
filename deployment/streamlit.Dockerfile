FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ../requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	gcc \
	g++ \
	libglib2.0-0 \
	libsm6 \
	libxrender1 \
	libxext6 \
	zlib1g-dev \
	libjpeg-dev \
	libpng-dev \
	libfreetype6-dev \
	pkg-config \
	libopenblas-dev \
	&& rm -rf /var/lib/apt/lists/*

# Upgrade pip and wheel
RUN python -m pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

# copy only the app folder at runtime via volume, but provide a default entrypoint
CMD ["streamlit", "run", "/app/app_streamlit.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
