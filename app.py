import os
import random

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

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
    return jsonify({"success": True, "prize": winner})


@app.route("/api/prizes", methods=["GET"])
def get_prizes():
    """取得預設獎品列表"""
    return jsonify({"prizes": DEFAULT_PRIZES})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)
