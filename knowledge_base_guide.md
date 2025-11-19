# 知識ベース永続保存ガイド

このガイドでは、SQLiteデータベースを使用して情報を永続的に保存し、自動的にLLMの応答に反映させる方法を説明します。

## 概要

知識ベース機能により、以下のことが可能になります：

- ✅ 情報を永続的に保存（データベースに保存）
- ✅ 保存した情報が自動的にLLMの応答に反映される
- ✅ カテゴリ別に情報を管理
- ✅ 情報の追加・取得・削除が簡単

## APIエンドポイント

### 1. 知識を保存する

```bash
curl -X POST "http://localhost:8000/knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "会社情報",
    "title": "会社概要",
    "content": "株式会社テック、設立2020年、従業員50名、主な事業はAI開発"
  }'
```

**レスポンス:**
```json
{
  "status": "saved",
  "id": 1,
  "item": {
    "category": "会社情報",
    "title": "会社概要",
    "content": "株式会社テック、設立2020年、従業員50名、主な事業はAI開発"
  }
}
```

### 2. 保存された知識を取得する

```bash
# すべての知識を取得
curl "http://localhost:8000/knowledge"

# 特定のカテゴリの知識を取得
curl "http://localhost:8000/knowledge?category=会社情報"
```

**レスポンス:**
```json
{
  "count": 2,
  "items": [
    {
      "id": 1,
      "category": "会社情報",
      "title": "会社概要",
      "content": "株式会社テック、設立2020年、従業員50名、主な事業はAI開発",
      "created_at": "2024-01-15 10:30:00"
    }
  ]
}
```

### 3. 特定の知識を取得する

```bash
curl "http://localhost:8000/knowledge/1"
```

### 4. 知識を削除する

```bash
curl -X DELETE "http://localhost:8000/knowledge/1"
```

### 5. カテゴリ一覧を取得する

```bash
curl "http://localhost:8000/knowledge/categories"
```

**レスポンス:**
```json
{
  "categories": ["会社情報", "製品情報", "FAQ"]
}
```

## 知識ベースを自動的に使用する

`/generate`エンドポイントで、保存された知識が自動的にコンテキストに追加されます。

### 基本的な使用（知識ベース自動使用）

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "私の会社について教えてください",
    "max_length": 200
  }'
```

**注意:** `use_knowledge`はデフォルトで`true`なので、上記のリクエストで自動的に知識ベースが使用されます。

### 知識ベースを使用しない場合

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "こんにちは",
    "use_knowledge": false,
    "max_length": 100
  }'
```

### 特定のカテゴリの知識のみを使用

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "製品について教えてください",
    "knowledge_category": "製品情報",
    "max_length": 200
  }'
```

## 実践的な使用例

### ステップ1: 知識を保存

```bash
# 会社情報を保存
curl -X POST "http://localhost:8000/knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "会社情報",
    "title": "会社概要",
    "content": "株式会社テック、設立2020年、従業員50名、主な事業はAI開発"
  }'

# 製品情報を保存
curl -X POST "http://localhost:8000/knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "製品情報",
    "title": "AIアシスタントPro",
    "content": "製品名: AIアシスタントPro、価格: 月額9800円、機能: 自然言語処理、画像認識、音声認識"
  }'

# FAQを保存
curl -X POST "http://localhost:8000/knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "FAQ",
    "title": "休暇制度",
    "content": "有給休暇は入社時に10日付与、年次有給休暇は勤続年数に応じて増加。特別休暇: 結婚休暇3日、出産休暇、育児休暇あり"
  }'
```

### ステップ2: 知識ベースを使用して質問

```bash
# 会社について質問（自動的に知識ベースが使用される）
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "会社の従業員数と事業内容を教えてください",
    "max_length": 200
  }'

# 製品について質問（製品情報カテゴリのみ使用）
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "製品の価格と機能を教えてください",
    "knowledge_category": "製品情報",
    "max_length": 200
  }'
```

## Pythonでの使用例

```python
import requests

# 知識を保存
response = requests.post(
    "http://localhost:8000/knowledge",
    json={
        "category": "会社情報",
        "title": "会社概要",
        "content": "株式会社テック、設立2020年、従業員50名"
    }
)
print(response.json())

# 保存された知識を取得
response = requests.get("http://localhost:8000/knowledge")
print(response.json())

# 知識ベースを使用して質問
response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "会社について教えてください",
        "max_length": 200
    }
)
print(response.json())
```

## データベースファイル

知識は`knowledge.db`というSQLiteデータベースファイルに保存されます。

- **場所**: プロジェクトルートディレクトリ
- **形式**: SQLite3
- **永続化**: サーバーを再起動してもデータは保持されます

### Dockerを使用している場合

Dockerコンテナ内でデータベースが作成されます。データを永続化するには、ボリュームマウントを使用してください：

```bash
# データディレクトリをマウント（推奨）
docker run -p 8000:8000 -p 11434:11434 \
  -v $(pwd)/data:/app/data \
  --rm llm-api
```

これにより、`./data/knowledge.db`にデータベースファイルが保存され、コンテナを再起動してもデータが保持されます。

## ベストプラクティス

1. **カテゴリを活用**: 関連する情報は同じカテゴリにまとめる
2. **明確なタイトル**: 検索しやすいように明確なタイトルを付ける
3. **簡潔な内容**: 各知識項目は簡潔にまとめる
4. **定期的な整理**: 不要になった知識は削除する

## 注意事項

- 知識ベースは**すべての知識を一度に**コンテキストに追加します
- 大量の知識がある場合は、`knowledge_category`で絞り込むことを推奨します
- データベースファイル（`knowledge.db`）はバックアップを取ることを推奨します

## トラブルシューティング

### データベースが作成されない

- サーバーの起動ログで「✅ 知識ベースデータベースを初期化しました」が表示されているか確認
- ファイルの書き込み権限を確認

### 知識が反映されない

- `use_knowledge: true`が設定されているか確認（デフォルトでtrue）
- 知識が実際に保存されているか`GET /knowledge`で確認

### Dockerでデータが消える

- ボリュームマウントを使用してデータベースファイルを永続化してください


