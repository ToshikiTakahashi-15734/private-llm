# ローカルAI - Ollamaを使用したLLM APIサーバー

Ollamaを使用してローカル環境でLLM（大規模言語モデル）を実行するためのAPIサーバーです。知識ベース機能により、情報を永続的に保存し、自動的にLLMの応答に反映させることができます。

## 特徴

- ✅ **Ollama統合**: ローカルでLLMを実行
- ✅ **知識ベース機能**: SQLiteを使用した永続的な情報保存
- ✅ **自動モデルインストール**: 起動時に自動的にモデルをインストール
- ✅ **ストリーミング対応**: リアルタイムで応答を取得
- ✅ **RESTful API**: FastAPIによるシンプルなAPI
- ✅ **Docker対応**: 簡単にセットアップ可能

## 必要な環境

- Docker Desktop（またはDocker Engine）がインストールされていること
- インターネット接続（初回起動時にモデルをダウンロードします）
- 最低4GB以上のメモリ推奨（モデルによって異なります）

## クイックスタート

### 1. リポジトリのクローン

```bash
git clone <リポジトリURL>
cd ローカルAI
```

### 2. Dockerイメージのビルド

```bash
docker build -t llm-api .
```

**初回はモデルのダウンロードに時間がかかります（10-20分程度）。**

### 3. コンテナの起動

```bash
# データベースを永続化する場合（推奨）
docker run -p 8000:8000 -p 11434:11434 \
  -v $(pwd)/data:/app/data \
  --rm llm-api
```

### 4. APIにアクセス

- **APIドキュメント**: http://localhost:8000/docs
- **ヘルスチェック**: http://localhost:8000/health

## 基本的な使い方

### テキスト生成

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "こんにちは、元気ですか？", "max_length": 100}'
```

### 知識を保存

```bash
curl -X POST "http://localhost:8000/knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "プロジェクト情報",
    "title": "設計者",
    "content": "設計者は高橋俊貴です"
  }'
```

### 保存した知識を使用して質問

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "このプロジェクトの設計者は誰ですか？", "max_length": 150}'
```

## 主な機能

### 1. テキスト生成 (`POST /generate`)

- 通常の生成
- ストリーミング生成
- システムプロンプト指定
- コンテキスト情報の追加
- 会話履歴の管理
- 知識ベースの自動使用

### 2. 知識ベース管理 (`/knowledge`)

- **POST /knowledge**: 知識を保存
- **GET /knowledge**: 保存された知識を取得
- **GET /knowledge/{id}**: 特定の知識を取得
- **DELETE /knowledge/{id}**: 知識を削除
- **GET /knowledge/categories**: カテゴリ一覧を取得

### 3. その他

- **GET /health**: ヘルスチェック
- **GET /models**: 利用可能なモデル一覧

## 詳細なドキュメント

- [プロンプト例](prompt_examples.md) - 様々なプロンプトの使用例
- [知識ベースガイド](knowledge_base_guide.md) - 知識ベースの使い方
- [学習例](learning_examples.md) - 情報を学習させる方法

## 環境変数

以下の環境変数を設定できます：

- `OLLAMA_BASE_URL`: OllamaサーバーのURL（デフォルト: `http://localhost:11434`）
- `OLLAMA_MODEL`: デフォルトで使用するモデル名（デフォルト: `llama3.2`）

```bash
docker run -p 8000:8000 -p 11434:11434 \
  -v $(pwd)/data:/app/data \
  -e OLLAMA_MODEL=qwen2.5:7b \
  --rm llm-api
```

## 推奨モデル

### 日本語対応モデル
- `llama3.2` - デフォルト、バランスが良い
- `qwen2.5:7b` - 高品質な日本語対応
- `gemma2:2b` - 軽量で高速

### 軽量モデル（メモリが少ない場合）
- `phi3:mini` - 非常に軽量
- `gemma2:2b` - バランスが良い

モデルのインストールは起動時に自動的に行われます。

## トラブルシューティング

### Dockerデーモンが起動していない

```bash
# Docker Desktopを起動してください
open -a Docker
```

### データベースエラー

データディレクトリをマウントしているか確認：

```bash
docker run -p 8000:8000 -p 11434:11434 \
  -v $(pwd)/data:/app/data \
  --rm llm-api
```

### モデルが見つからない

起動時に自動的にインストールされますが、手動でインストールする場合：

```bash
docker exec <コンテナ名> ollama pull llama3.2
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

プルリクエストやイシューの報告を歓迎します。

## 作者

設計者: 高橋俊貴
