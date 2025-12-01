import os
import random

import psycopg2
from flask import Flask, jsonify, render_template, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# PostgreSQL 連線設定 - 使用 Zeabur 環境變數
DATABASE_URL = os.environ.get("POSTGRES_URI") or os.environ.get("POSTGRES_CONNECTION_STRING")


def get_db_connection():
    """取得資料庫連線"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn


def init_db():
    """初始化資料庫表格"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lottery_results (
            id SERIAL PRIMARY KEY,
            prize_name VARCHAR(100) NOT NULL,
            prize_emoji VARCHAR(10) NOT NULL,
            prize_rarity VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


# 應用程式啟動時初始化資料庫
try:
    init_db()
    print("資料庫初始化成功")
except Exception as e:
    print(f"資料庫初始化失敗: {e}")

# 預設獎品列表
DEFAULT_PRIZES = [
    {"name": "超級蘑菇", "emoji": "🍄", "rarity": "common"},
    {"name": "火焰花", "emoji": "🌸", "rarity": "common"},
    {"name": "無敵星星", "emoji": "⭐", "rarity": "rare"},
    {"name": "1UP蘑菇", "emoji": "💚", "rarity": "rare"},
    {"name": "金幣x100", "emoji": "🪙", "rarity": "common"},
    {"name": "藍色龜殼", "emoji": "🐢", "rarity": "common"},
    {"name": "雲朵", "emoji": "☁️", "rarity": "rare"},
    {"name": "彩虹之路通行證", "emoji": "🌈", "rarity": "legendary"},
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/draw", methods=["POST"])
def draw_prize():
    """抽獎 API"""
    data = request.get_json() or {}
    prizes = data.get("prizes", DEFAULT_PRIZES)

    if not prizes:
        return jsonify({"error": "沒有可抽的獎品"}), 400

    # 根據稀有度調整機率
    weighted_prizes = []
    for prize in prizes:
        rarity = prize.get("rarity", "common")
        if rarity == "common":
            weight = 50
        elif rarity == "rare":
            weight = 30
        else:  # legendary
            weight = 10
        weighted_prizes.extend([prize] * weight)

    winner = random.choice(weighted_prizes)

    # 儲存抽獎結果到資料庫
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO lottery_results (prize_name, prize_emoji, prize_rarity) VALUES (%s, %s, %s)",
            (winner["name"], winner["emoji"], winner["rarity"]),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"儲存抽獎結果失敗: {e}")

    return jsonify({"success": True, "prize": winner})


@app.route("/api/prizes", methods=["GET"])
def get_prizes():
    """取得預設獎品列表"""
    return jsonify({"prizes": DEFAULT_PRIZES})


@app.route("/api/history", methods=["GET"])
def get_history():
    """取得抽獎歷史紀錄"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, prize_name, prize_emoji, prize_rarity, created_at
            FROM lottery_results
            ORDER BY created_at DESC
            LIMIT 50
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()

        # 轉換結果為可序列化的格式
        history = []
        for row in results:
            history.append(
                {
                    "id": row["id"],
                    "name": row["prize_name"],
                    "emoji": row["prize_emoji"],
                    "rarity": row["prize_rarity"],
                    "created_at": row["created_at"].isoformat()
                    if row["created_at"]
                    else None,
                }
            )

        return jsonify({"success": True, "history": history})
    except Exception as e:
        print(f"取得歷史紀錄失敗: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/history")
def history_page():
    """抽獎歷史紀錄頁面"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, prize_name, prize_emoji, prize_rarity, created_at
            FROM lottery_results
            ORDER BY created_at DESC
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("history.html", records=results)
    except Exception as e:
        print(f"取得歷史紀錄失敗: {e}")
        return render_template("history.html", records=[], error=str(e))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)
