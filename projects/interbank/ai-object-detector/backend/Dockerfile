# Python 3.11を使用
FROM python:3.11-slim

WORKDIR /app

# AI（OpenCV）の実行に必要なシステムパッケージをインストール
# OSのライブラリを更新し、AI（OpenCV）に必要な依存パッケージをインストール
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# FastAPIを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]