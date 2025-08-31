# ベースイメージ
FROM python:3.10-slim

# 作業ディレクトリ
WORKDIR /app

# 依存関係コピー & インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコピー
COPY . .

# 実行コマンド
CMD ["python", "main.py"]
