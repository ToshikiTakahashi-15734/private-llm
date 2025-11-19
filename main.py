#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Web API: Ollamaを使用したLLM APIサーバー
ブラウザやcurlからアクセスできるLLM APIを提供します
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional, List
from pathlib import Path
import requests
import uvicorn
import json
import os
import sqlite3
from datetime import datetime

# Ollamaの設定
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")  # デフォルトモデル

# データベース設定
DB_DIR = Path("/app/data")
DB_PATH = DB_DIR / "knowledge.db"

# データベースディレクトリを作成（存在しない場合）
DB_DIR.mkdir(parents=True, exist_ok=True)

class Message(BaseModel):
    role: str  # "system", "user", "assistant"
    content: str

class TextRequest(BaseModel):
    prompt: str
    max_length: int = 100
    temperature: float = 0.7
    stream: bool = False
    model: Optional[str] = None  # 使用するモデル名（オプション）
    system: Optional[str] = None  # システムプロンプト（情報を学習させる場合に使用）
    context: Optional[str] = None  # 追加のコンテキスト情報
    messages: Optional[List[Message]] = None  # 会話履歴（複数のメッセージ）
    use_knowledge: bool = True  # 知識ベースを自動的に使用するか（デフォルト: True）
    knowledge_category: Optional[str] = None  # 特定のカテゴリの知識のみを使用

class TextResponse(BaseModel):
    generated_text: str
    prompt: str
    model: str

class KnowledgeItem(BaseModel):
    category: str
    title: str
    content: str

class KnowledgeItemResponse(BaseModel):
    id: int
    category: str
    title: str
    content: str
    created_at: str

def init_db():
    """データベースを初期化"""
    try:
        # データベースディレクトリが存在することを確認
        DB_DIR.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_category ON knowledge(category)
        """)
        conn.commit()
        conn.close()
        print(f"✅ 知識ベースデータベースを初期化しました: {DB_PATH}")
    except Exception as e:
        print(f"⚠️  データベースの初期化中にエラーが発生しました: {e}")
        print(f"   データベースパス: {DB_PATH}")
        print(f"   データベースディレクトリ: {DB_DIR}")
        import traceback
        traceback.print_exc()
        # エラーが発生してもアプリケーションは起動を続ける

def get_knowledge_from_db(category: Optional[str] = None) -> List[dict]:
    """データベースから知識を取得"""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        if category:
            cursor = conn.execute(
                "SELECT id, category, title, content, created_at FROM knowledge WHERE category = ? ORDER BY created_at DESC",
                (category,)
            )
        else:
            cursor = conn.execute(
                "SELECT id, category, title, content, created_at FROM knowledge ORDER BY created_at DESC"
            )
        
        items = []
        for row in cursor.fetchall():
            items.append({
                "id": row[0],
                "category": row[1],
                "title": row[2],
                "content": row[3],
                "created_at": row[4]
            })
        return items
    finally:
        conn.close()

def check_ollama_connection():
    """Ollamaサーバーへの接続を確認"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"⚠️  Ollamaサーバーに接続できません: {e}")
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーション起動時と終了時の処理"""
    # 起動時の処理
    try:
        print("=" * 60)
        print("Ollama API Server を起動します")
        print("=" * 60)
        print(f"\nOllama URL: {OLLAMA_BASE_URL}")
        print(f"デフォルトモデル: {DEFAULT_MODEL}")
        
        # データベースを初期化
        init_db()
        
        # Ollamaサーバーへの接続を試行（最大5回、各3秒待機）
        max_retries = 5
        ollama_connected = False
        for i in range(max_retries):
            if check_ollama_connection():
                ollama_connected = True
                break
            if i < max_retries - 1:
                print(f"⏳ Ollamaサーバーへの接続を試行中... ({i+1}/{max_retries})")
                import time
                time.sleep(3)
        
        if ollama_connected:
            print("✅ Ollamaサーバーに接続できました")
            # 利用可能なモデル一覧を取得
            try:
                response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    if models:
                        print(f"\n利用可能なモデル:")
                        for model in models:
                            print(f"  - {model.get('name', 'unknown')}")
                    else:
                        print(f"\n⚠️  モデルがインストールされていません")
                        print(f"   起動スクリプトが自動的にインストールします...")
            except Exception as e:
                print(f"⚠️  モデル一覧の取得に失敗: {e}")
        else:
            print("⚠️  Ollamaサーバーに接続できませんでした")
            print(f"   起動スクリプトがOllamaサーバーを起動している可能性があります")
            print(f"   しばらく待ってから再度試してください")
        
        print("\n" + "=" * 60)
        print("✅ アプリケーションの起動が完了しました")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"❌ 起動時にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        # エラーが発生してもアプリケーションは起動を続ける
    
    yield  # アプリケーション実行中
    
    # 終了時の処理（必要に応じて追加）

app = FastAPI(title="LLM API Server (Ollama)", version="2.0.0", lifespan=lifespan)

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "LLM API Server (Ollama)",
        "ollama_url": OLLAMA_BASE_URL,
        "default_model": DEFAULT_MODEL,
        "endpoints": {
            "/generate": "POST - テキスト生成（streamオプションでストリーミング可能、system/context/messagesで情報を学習可能、use_knowledgeで知識ベース自動使用）",
            "/health": "GET - ヘルスチェック",
            "/models": "GET - 利用可能なモデル一覧",
            "/knowledge": "GET/POST/DELETE - 知識ベースの管理（永続保存）"
        }
    }

@app.get("/health")
async def health():
    """ヘルスチェック"""
    ollama_connected = check_ollama_connection()
    return {
        "status": "healthy" if ollama_connected else "ollama_not_connected",
        "ollama_connected": ollama_connected,
        "ollama_url": OLLAMA_BASE_URL,
        "default_model": DEFAULT_MODEL
    }

@app.get("/models")
async def list_models():
    """利用可能なモデル一覧を取得"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=503, detail="Ollamaサーバーに接続できません")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Ollamaサーバーへの接続エラー: {str(e)}")

# 知識ベース管理API
@app.post("/knowledge", response_model=dict)
async def save_knowledge(item: KnowledgeItem):
    """知識を保存（永続化）"""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        cursor = conn.execute(
            "INSERT INTO knowledge (category, title, content) VALUES (?, ?, ?)",
            (item.category, item.title, item.content)
        )
        conn.commit()
        knowledge_id = cursor.lastrowid
        return {
            "status": "saved",
            "id": knowledge_id,
            "item": {
                "category": item.category,
                "title": item.title,
                "content": item.content
            }
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"知識の保存に失敗しました: {str(e)}")
    finally:
        conn.close()

@app.get("/knowledge", response_model=dict)
async def get_knowledge(category: Optional[str] = None):
    """保存された知識を取得"""
    try:
        items = get_knowledge_from_db(category)
        return {
            "count": len(items),
            "items": items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知識の取得に失敗しました: {str(e)}")

@app.get("/knowledge/{knowledge_id}", response_model=KnowledgeItemResponse)
async def get_knowledge_by_id(knowledge_id: int):
    """特定のIDの知識を取得"""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        cursor = conn.execute(
            "SELECT id, category, title, content, created_at FROM knowledge WHERE id = ?",
            (knowledge_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="知識が見つかりません")
        
        return {
            "id": row[0],
            "category": row[1],
            "title": row[2],
            "content": row[3],
            "created_at": row[4]
        }
    finally:
        conn.close()

@app.delete("/knowledge/{knowledge_id}")
async def delete_knowledge(knowledge_id: int):
    """知識を削除"""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        cursor = conn.execute("DELETE FROM knowledge WHERE id = ?", (knowledge_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="知識が見つかりません")
        return {"status": "deleted", "id": knowledge_id}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"知識の削除に失敗しました: {str(e)}")
    finally:
        conn.close()

@app.get("/knowledge/categories", response_model=dict)
async def get_categories():
    """利用可能なカテゴリ一覧を取得"""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        cursor = conn.execute("SELECT DISTINCT category FROM knowledge ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        return {"categories": categories}
    finally:
        conn.close()

def _build_prompt(request: TextRequest) -> str:
    """プロンプトを構築（システムプロンプト、コンテキスト、会話履歴、知識ベースを含む）"""
    parts = []
    
    # システムプロンプトを追加
    if request.system:
        parts.append(f"システム: {request.system}\n")
    
    # 知識ベースから情報を取得して追加
    if request.use_knowledge:
        knowledge_items = get_knowledge_from_db(request.knowledge_category)
        if knowledge_items:
            knowledge_text = "保存された知識ベース:\n"
            for item in knowledge_items:
                knowledge_text += f"- [{item['category']}] {item['title']}: {item['content']}\n"
            parts.append(f"{knowledge_text}\n")
    
    # 追加のコンテキスト情報を追加
    if request.context:
        parts.append(f"コンテキスト情報:\n{request.context}\n")
    
    # 会話履歴がある場合
    if request.messages:
        for msg in request.messages:
            if msg.role == "system":
                parts.append(f"システム: {msg.content}\n")
            elif msg.role == "user":
                parts.append(f"ユーザー: {msg.content}\n")
            elif msg.role == "assistant":
                parts.append(f"アシスタント: {msg.content}\n")
        # 最後にユーザーのプロンプトを追加
        parts.append(f"ユーザー: {request.prompt}\nアシスタント:")
    else:
        # 通常のプロンプト
        parts.append(request.prompt)
    
    return "".join(parts)

@app.post("/generate", response_model=TextResponse)
async def generate_text(request: TextRequest):
    """テキスト生成エンドポイント"""
    try:
        # 使用するモデルを決定
        model_name = request.model or DEFAULT_MODEL
        
        # プロンプトを構築
        full_prompt = _build_prompt(request)
        
        # ストリーミングがリクエストされた場合
        if request.stream:
            return StreamingResponse(
                _generate_stream(request, model_name, full_prompt),
                media_type="text/event-stream"
            )
        
        # Ollama APIにリクエストを送信
        ollama_url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": model_name,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_length,  # Ollamaではnum_predictを使用
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=300)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Ollama API エラー: {response.text}"
            )
        
        result = response.json()
        generated_text = result.get("response", "")
        
        return TextResponse(
            prompt=request.prompt,
            generated_text=generated_text,
            model=model_name
        )
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollamaサーバーへの接続エラー: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _generate_stream(request: TextRequest, model_name: str, full_prompt: str):
    """ストリーミング生成（ジェネレータ）"""
    try:
        ollama_url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": model_name,
            "prompt": full_prompt,
            "stream": True,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_length,
            }
        }
        
        response = requests.post(ollama_url, json=payload, stream=True, timeout=300)
        
        if response.status_code != 200:
            yield f"data: {json.dumps({'error': f'Ollama API エラー: {response.text}'}, ensure_ascii=False)}\n\n"
            return
        
        full_text = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if "response" in data:
                        chunk = data["response"]
                        full_text += chunk
                        yield f"data: {json.dumps({'text': chunk, 'full_text': full_text, 'done': data.get('done', False)}, ensure_ascii=False)}\n\n"
        
                    if data.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue
        
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

if __name__ == "__main__":
    print("\nアクセス方法:")
    print("  - APIドキュメント: http://localhost:8000/docs")
    print("  - ヘルスチェック: http://localhost:8000/health")
    print("  - テキスト生成: POST http://localhost:8000/generate")
    print("  - モデル一覧: GET http://localhost:8000/models")
    print("  - 知識ベース管理:")
    print("    - 知識保存: POST http://localhost:8000/knowledge")
    print("    - 知識取得: GET http://localhost:8000/knowledge")
    print("    - 知識削除: DELETE http://localhost:8000/knowledge/{id}")
    print("\n例（通常）:")
    print('  curl -X POST "http://localhost:8000/generate" \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"prompt": "こんにちは、元気ですか？", "max_length": 100}\'')
    print("\n例（ストリーミング）:")
    print('  curl -X POST "http://localhost:8000/generate" \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"prompt": "こんにちは、元気ですか？", "max_length": 100, "stream": true}\'')
    print("\n例（特定のモデルを指定）:")
    print('  curl -X POST "http://localhost:8000/generate" \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"prompt": "Hello", "model": "llama3.2", "max_length": 100}\'')
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
