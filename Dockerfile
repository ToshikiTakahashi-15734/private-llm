# LLM Web API用: Ollamaを使用したLLM APIサーバー
FROM python:3.10-slim

WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Ollamaをインストール
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pythonライブラリをインストール
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# コードと起動スクリプトをコピー
COPY main.py /app/main.py
COPY start.sh /app/start.sh

# 起動スクリプトに実行権限を付与
RUN chmod +x /app/start.sh

# データベースディレクトリを作成
RUN mkdir -p /app/data

# ポートを公開
EXPOSE 8000
EXPOSE 11434

# OllamaサーバーとAPIサーバーを起動
# 起動スクリプトを使用（モデルの自動インストール含む）
CMD ["/app/start.sh"]

