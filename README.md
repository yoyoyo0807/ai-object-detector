# 🐾 AI Object Detector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Terraform](https://img.shields.io/badge/Terraform-1.5+-623CE4.svg?style=flat&logo=Terraform&logoColor=white)](https://www.terraform.io/)

最新の物体検出モデル **YOLO** を活用し、Webブラウザから画像をアップロードするだけで瞬時に物体を検出し可視化するフルスタックアプリケーションです。AWS Fargate を利用したスケーラブルなインフラ構成を Terraform で管理しています。



## 🚀 主な機能
- **リアルタイム物体検出**: YOLOv11 モデルによる高速かつ高精度な物体認識
- **直感的なWebインターフェース**: Next.js を使用したモダンなUI
- **スケーラブルなバックエンド**: FastAPI を ECS Fargate 上で動作させ、リソースを最適化
- **Infrastructure as Code**: Terraform によるインフラの完全自動構築

## 🏗️ システムアーキテクチャ
本アプリは以下の技術スタックで構成されています。

- **Frontend**: Next.js (TypeScript), Tailwind CSS
- **Backend**: FastAPI (Python), PyTorch, YOLO
- **Infrastructure**: AWS (ECS Fargate, ALB, ECR, CloudWatch Logs)
- **IAC**: Terraform
- **Container**: Docker

## 🛠️ セットアップとデプロイ

### 前提条件
- Docker & Docker Compose
- AWS CLI (設定済みであること)
- Terraform

### ローカル実行 (Backend)
```bash
cd backend
pip install -r requirements.txt
python main.py
