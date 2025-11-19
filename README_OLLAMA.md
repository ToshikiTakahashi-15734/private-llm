# Ollamaを使用したローカルAI APIサーバー

このプロジェクトは、[Ollama](https://ollama.com/)を使用してローカル環境でLLM（大規模言語モデル）を実行するためのセットアップです。

## Ollamaとは

Ollamaは、ローカルでLLMを実行するためのツールです。以下の利点があります：

- **簡単なモデル管理**: `ollama pull`コマンドでモデルを簡単にインストール
- **メモリ効率**: 最適化された実行環境
- **複数モデルの切り替え**: 複数のモデルを簡単に切り替え可能
- **シンプルなAPI**: RESTful APIで簡単にアクセス

## 必要な環境

- Python 3.10以上
- Ollamaがインストールされていること（またはDockerを使用）
- インターネット接続（初回起動時にモデルをダウンロードします）
- 最低4GB以上のメモリ推奨

## セットアップ手順

### 方法1: Ollamaを直接インストール（推奨）

#### 1. Ollamaのインストール

macOS:
```bash
brew install ollama
```

または、[公式サイト](https://ollama.com/download)からダウンロード

#### 2. Ollamaサーバーの起動

```bash
ollama serve
```

別のターミナルで、モデルをインストール：
```bash
# 日本語対応モデルの例
ollama pull llama3.2
ollama pull qwen2.5:7b
ollama pull gemma2:2b

# または、より軽量なモデル
ollama pull phi3:mini
```

#### 3. Python環境のセットアップ

```bash
pip install -r requirements_ollama.txt
```

#### 4. APIサーバーの起動

```bash
python main_ollama.py
```

### 方法2: Dockerを使用

#### 1. Dockerイメージのビルド

```bash
docker build -f Dockerfile.ollama -t llm-api-ollama .
```

#### 2. コンテナの実行

```bash
docker run -p 8000:8000 -p 11434:11434 --rm llm-api-ollama
```

**注意**: Docker内でOllamaを使用する場合、モデルを事前にプルする必要があります。

## APIにアクセス

### ブラウザでアクセス
- APIドキュメント（Swagger UI）: http://localhost:8000/docs
- ヘルスチェック: http://localhost:8000/health
- モデル一覧: http://localhost:8000/models

### curlでテキスト生成

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "こんにちは、元気ですか？", "max_length": 100}'
```

### ストリーミング

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "こんにちは、元気ですか？", "max_length": 100, "stream": true}'
```

### 特定のモデルを指定

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?", "model": "llama3.2", "max_length": 100}'
```

## APIエンドポイント

### POST /generate
テキストを生成します。

**リクエストボディ:**
```json
{
  "prompt": "Your text prompt here",
  "max_length": 100,
  "temperature": 0.7,
  "stream": false,
  "model": "llama3.2"
}
```

**パラメータ:**
- `prompt` (必須): 生成の開始となるテキスト
- `max_length` (オプション): 生成する最大トークン数（デフォルト: 100）
- `temperature` (オプション): 生成のランダム性（デフォルト: 0.7）
- `stream` (オプション): ストリーミング応答を有効にする（デフォルト: false）
- `model` (オプション): 使用するモデル名（デフォルト: 環境変数`OLLAMA_MODEL`または`llama3.2`）

**レスポンス:**
```json
{
  "prompt": "Your text prompt here",
  "generated_text": "Generated continuation...",
  "model": "llama3.2"
}
```

### GET /health
サーバーの状態を確認します。

### GET /models
利用可能なモデル一覧を取得します。

## 環境変数

以下の環境変数を設定できます：

- `OLLAMA_BASE_URL`: OllamaサーバーのURL（デフォルト: `http://localhost:11434`）
- `OLLAMA_MODEL`: デフォルトで使用するモデル名（デフォルト: `llama3.2`）

例：
```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=qwen2.5:7b
python main_ollama.py
```

## 推奨モデル

### 日本語対応モデル
- `qwen2.5:7b` - 高品質な日本語対応モデル
- `llama3.2` - Metaの最新モデル（日本語も対応）
- `gemma2:2b` - 軽量で高速

### 軽量モデル（メモリが少ない場合）
- `phi3:mini` - 非常に軽量
- `gemma2:2b` - バランスが良い

### 高性能モデル（メモリが十分な場合）
- `qwen2.5:14b` - 高品質
- `llama3.1:8b` - 高性能

モデルのインストール：
```bash
ollama pull <モデル名>
```

## トラブルシューティング

### Ollamaサーバーに接続できない場合

1. Ollamaサーバーが起動しているか確認：
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. 別のURLを使用する場合、環境変数を設定：
   ```bash
   export OLLAMA_BASE_URL=http://your-ollama-server:11434
   ```

### モデルが見つからない場合

モデルをインストール：
```bash
ollama pull llama3.2
```

利用可能なモデルを確認：
```bash
ollama list
```

### メモリ不足エラーが発生した場合

より軽量なモデルを使用してください：
```bash
ollama pull phi3:mini
```

## 元の実装との比較

| 項目 | 元の実装 (Transformers) | Ollama版 |
|------|------------------------|----------|
| モデル管理 | 手動でダウンロード | `ollama pull`で簡単 |
| メモリ使用量 | 高め（モデルを直接ロード） | 最適化されている |
| モデル切り替え | コード変更が必要 | APIで簡単に切り替え |
| セットアップ | 複雑 | シンプル |
| カスタマイズ | 柔軟 | 制限あり |

## 次のステップ

- 複数のモデルを試す
- ストリーミング応答を活用する
- 会話履歴の管理機能を追加する
- 認証機能を追加する




