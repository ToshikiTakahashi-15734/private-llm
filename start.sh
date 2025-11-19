#!/bin/bash
# OllamaサーバーとAPIサーバーの起動スクリプト

# Ollamaサーバーをバックグラウンドで起動
echo "🚀 Ollamaサーバーを起動しています..."
ollama serve &
OLLAMA_PID=$!

# Ollamaサーバーが起動するまで待機（最大30秒）
echo "⏳ Ollamaサーバーの起動を待機しています..."
for i in {1..10}; do
    # ollama listコマンドでサーバーが起動しているか確認
    if ollama list > /dev/null 2>&1; then
        echo "✅ Ollamaサーバーが起動しました"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "⚠️  Ollamaサーバーの起動に時間がかかっていますが、続行します..."
    fi
    sleep 3
done

# デフォルトモデルを環境変数から取得（デフォルト: llama3.2）
MODEL=${OLLAMA_MODEL:-llama3.2}

# モデルがインストールされているか確認
echo "モデル ${MODEL} のインストール状況を確認しています..."
if ollama list | grep -q "${MODEL}"; then
    echo "✅ モデル ${MODEL} は既にインストールされています"
else
    echo "📥 モデル ${MODEL} をインストールしています（初回は時間がかかります）..."
    ollama pull ${MODEL}
    if [ $? -eq 0 ]; then
        echo "✅ モデル ${MODEL} のインストールが完了しました"
    else
        echo "⚠️  モデル ${MODEL} のインストールに失敗しました"
    fi
fi

# APIサーバーを起動
echo "🚀 APIサーバーを起動しています..."
python main.py

