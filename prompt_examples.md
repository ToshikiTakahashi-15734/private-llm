# Ollama LLM API プロンプト例

Ollamaを使用したLLM APIサーバーでの様々なプロンプトの例です。

## 基本的な対話

### 挨拶
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "こんにちは、元気ですか？", "max_length": 100}'
```

### 自己紹介
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "自己紹介をお願いします", "max_length": 150}'
```

## 質問・相談

### 健康に関する相談
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "最近疲れやすくて、どうすればいいですか？", "max_length": 150}'
```

### 学習・勉強の相談
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "プログラミングを始めたいのですが、何から始めればいいですか？", "max_length": 200}'
```

### 仕事の相談
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "プレゼンテーションで緊張してしまいます。どうすればいいですか？", "max_length": 150}'
```

## 創造的なタスク

### ストーリー生成
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "未来の東京を舞台にした短い物語を書いてください", "max_length": 300, "temperature": 0.9}'
```

### アイデア出し
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "新しいWebサービスのアイデアを3つ考えてください", "max_length": 250}'
```

### レシピ提案
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "簡単に作れるおいしい料理のレシピを教えてください", "max_length": 200}'
```

## 技術的な質問

### プログラミング
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Pythonでリストをソートする方法を教えてください", "max_length": 150}'
```

### システム設計
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "スケーラブルなWebアプリケーションの設計について教えてください", "max_length": 250}'
```

## 日常会話

### 天気の話題
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "今日はいい天気ですね", "max_length": 100}'
```

### 趣味の話
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "最近どんな趣味にはまっていますか？", "max_length": 150}'
```

## 英語での対話

### 英語での質問
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the benefits of learning a new language?", "max_length": 200}'
```

### 英語での会話
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me about your favorite book", "max_length": 150}'
```

## パラメータの調整

### 創造的な応答（temperatureを高く）
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "面白いジョークを教えてください", "max_length": 150, "temperature": 0.9}'
```

### 確定的な応答（temperatureを低く）
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "2+2は何ですか？", "max_length": 50, "temperature": 0.3}'
```

### 長い応答（max_lengthを大きく）
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "人工知能の未来について詳しく説明してください", "max_length": 500, "temperature": 0.7}'
```

## プロンプトのコツ

1. **明確な質問**: 具体的で明確な質問をすると、より良い応答が得られます
2. **コンテキストの提供**: 必要な背景情報を含めると、より適切な応答が得られます
3. **温度の調整**: 
   - `temperature: 0.3-0.5` → 確定的で一貫性のある応答
   - `temperature: 0.7-0.9` → 創造的で多様な応答
4. **長さの調整**: 
   - 短い応答: `max_length: 50-100`
   - 中程度: `max_length: 100-200`
   - 長い応答: `max_length: 200-500`

## Ollama特有の機能

### 特定のモデルを指定

```bash
# llama3.2モデルを使用
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "こんにちは、元気ですか？", "model": "llama3.2", "max_length": 100}'

# qwen2.5:7bモデルを使用
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Pythonの基礎を教えてください", "model": "qwen2.5:7b", "max_length": 200}'
```

### ストリーミング応答

リアルタイムで応答を取得できます：

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "人工知能の未来について説明してください", "max_length": 300, "stream": true}'
```

## 例：会話の続き

複数回のやり取りで会話を続けることもできます：

```bash
# 1回目
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "こんにちは", "max_length": 100}'

# 2回目（前の応答を考慮して続ける）
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "今日は何をしていますか？", "max_length": 100}'
```

## 利用可能なモデルの確認

インストール済みのモデル一覧を確認：

```bash
curl http://localhost:8000/models
```

またはブラウザで：
http://localhost:8000/models

