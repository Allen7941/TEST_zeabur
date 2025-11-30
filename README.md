# Mario 抽獎機 🍄

一個以 Super Mario 風格設計的網頁抽獎工具，使用 Flask 框架開發，支援部署到 Zeabur。

## 功能特色

- 🎮 經典 Mario 遊戲風格介面
- ❓ 點擊問號方塊抽獎
- 🏆 三種稀有度獎品：普通、稀有、傳說
- 📜 抽獎歷史紀錄
- 🪙 抽獎次數統計
- 📱 響應式設計，支援手機瀏覽

## 技術棧

- **後端**: Python + Flask
- **前端**: HTML5 + CSS3 + JavaScript
- **套件管理**: UV
- **生產伺服器**: Gunicorn
- **部署平台**: Zeabur

## 本地開發

### 安裝依賴

```bash
uv sync
```

### 啟動開發伺服器

```bash
uv run python app.py
```

然後開啟瀏覽器訪問 http://localhost:5000

## 部署到 Zeabur

1. 將專案推送到 GitHub
2. 在 Zeabur 控制台建立新專案
3. 連結你的 GitHub 儲存庫
4. Zeabur 會自動偵測並部署

## 專案結構

```
mario-lottery/
├── app.py              # Flask 主程式
├── pyproject.toml      # UV 專案設定
├── uv.lock             # 依賴鎖定檔
├── zeabur.json         # Zeabur 部署設定
├── Procfile            # 生產環境啟動指令
├── templates/
│   └── index.html      # 網頁模板
└── static/
    ├── style.css       # 樣式表
    └── script.js       # 前端腳本
```

## 授權

MIT License
