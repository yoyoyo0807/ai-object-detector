# Node.jsを使用
FROM node:18-alpine

WORKDIR /app

# 依存関係のインストール
COPY package*.json ./
RUN npm install

# ソースコードをコピー
COPY . .

# 開発用サーバーを起動
CMD ["npm", "run", "dev"]