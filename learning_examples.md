# 情報を学習させる方法

このドキュメントでは、LLMに情報を学習させる（コンテキストとして提供する）方法を説明します。

## 方法1: システムプロンプトを使用（推奨）

システムプロンプトを使用して、AIの役割や知識を定義します。

### 基本的な使用例

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "私の会社について教えてください",
    "system": "あなたは株式会社テックのカスタマーサポートです。会社の情報: 設立は2020年、従業員数は50名、主な事業はAI開発です。",
    "max_length": 200
  }'
```

### より詳細な情報を提供

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "製品の特徴を教えてください",
    "system": "あなたは製品サポートです。製品情報: 製品名はAIアシスタントPro、価格は月額9800円、主な機能は自然言語処理、画像認識、音声認識です。",
    "max_length": 200
  }'
```

## 方法2: コンテキスト情報を使用

追加のコンテキスト情報を提供して、より詳細な情報を学習させます。

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "最新のプロジェクトの進捗は？",
    "context": "プロジェクトA: 進捗率80%、完了予定は来月15日。プロジェクトB: 進捗率45%、完了予定は3ヶ月後。チームメンバー: 田中、佐藤、鈴木。",
    "max_length": 200
  }'
```

## 方法3: システムプロンプト + コンテキストの組み合わせ

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "顧客からの問い合わせに答えてください",
    "system": "あなたはカスタマーサポートです。丁寧で親切な対応を心がけてください。",
    "context": "顧客情報: 山田太郎様、会員番号12345、契約プランはプレミアム、契約日は2024年1月15日。",
    "max_length": 200
  }'
```

## 方法4: 会話履歴を使用（複数ターンの対話）

会話の流れを保持しながら、情報を段階的に学習させます。

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "それについて詳しく教えてください",
    "system": "あなたは技術サポートです。",
    "messages": [
      {"role": "user", "content": "Pythonのリストについて教えてください"},
      {"role": "assistant", "content": "Pythonのリストは、複数の値を順序付けて格納できるデータ構造です。"},
      {"role": "user", "content": "リストの操作について知りたいです"},
      {"role": "assistant", "content": "リストの主な操作には、append()、extend()、insert()、remove()などがあります。"}
    ],
    "max_length": 200
  }'
```

## 実践的な使用例

### 例1: 会社のFAQボット

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "休暇制度について教えてください",
    "system": "あなたは人事部のFAQボットです。以下の情報を基に回答してください。",
    "context": "休暇制度: 有給休暇は入社時に10日付与、年次有給休暇は勤続年数に応じて増加。特別休暇: 結婚休暇3日、出産休暇、育児休暇あり。夏季休暇: 8月中旬に5日間。",
    "max_length": 250
  }'
```

### 例2: 製品情報アシスタント

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "この製品の価格と機能を教えてください",
    "system": "あなたは製品情報アシスタントです。",
    "context": "製品名: AIチャットボット、価格: 月額9,800円（年払いで10%割引）、機能: 24時間対応、多言語対応、カスタマイズ可能、API連携可能、対応チャネル: Web、LINE、Slack、メール。",
    "max_length": 200
  }'
```

### 例3: 学習コンテンツの提供

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "このトピックについて説明してください",
    "system": "あなたは教育アシスタントです。分かりやすく説明してください。",
    "context": "トピック: 機械学習の基礎。機械学習は、データからパターンを学習して予測や分類を行う技術です。主な種類: 教師あり学習、教師なし学習、強化学習。",
    "max_length": 300
  }'
```

## Pythonでの使用例

```python
import requests

# システムプロンプトを使用
response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "会社の情報を教えてください",
        "system": "あなたは株式会社テックの社員です。会社情報: 設立2020年、従業員50名、事業はAI開発。",
        "max_length": 200
    }
)
print(response.json())

# 会話履歴を使用
response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "それについて詳しく",
        "system": "あなたは技術サポートです。",
        "messages": [
            {"role": "user", "content": "Pythonについて教えて"},
            {"role": "assistant", "content": "Pythonは高水準のプログラミング言語です。"}
        ],
        "max_length": 200
    }
)
print(response.json())
```

## ベストプラクティス

1. **システムプロンプト**: AIの役割や基本的な知識を定義
2. **コンテキスト**: 具体的なデータや情報を提供
3. **会話履歴**: 複数ターンの対話で段階的に情報を提供
4. **明確な指示**: どの情報を使うべきか明確に指定

## 注意事項

- 提供した情報は**そのリクエスト内でのみ有効**です（永続的な学習ではありません）
- 長いコンテキストは`max_length`を大きくしてください
- 複雑な情報は`system`と`context`を組み合わせて使用すると効果的です

## 高度な使い方: RAG（Retrieval-Augmented Generation）

大量のドキュメントから情報を検索して使用する場合は、ベクトルデータベース（例: Chroma、FAISS）と組み合わせることで、より高度な情報検索が可能です。これは別途実装が必要です。


