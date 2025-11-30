// DOM 元素
const questionBlock = document.getElementById('questionBlock');
const drawButton = document.getElementById('drawButton');
const prizePopup = document.getElementById('prizePopup');
const prizeEmoji = document.getElementById('prizeEmoji');
const prizeName = document.getElementById('prizeName');
const prizeRarity = document.getElementById('prizeRarity');
const historyList = document.getElementById('historyList');
const coinCount = document.getElementById('coin-count');

// 狀態
let isDrawing = false;
let totalDraws = 0;

// 稀有度對應文字
const rarityText = {
    common: '普通',
    rare: '稀有',
    legendary: '傳說'
};

// 抽獎函數
async function draw() {
    if (isDrawing) return;

    isDrawing = true;
    drawButton.disabled = true;

    // 隱藏之前的獎品
    prizePopup.classList.remove('show');

    // 方塊動畫
    questionBlock.classList.add('hit');

    // 播放音效（如果有的話）
    try {
        const coinSound = document.getElementById('coinSound');
        if (coinSound) {
            coinSound.currentTime = 0;
            coinSound.play().catch(() => { });
        }
    } catch (e) { }

    try {
        // 呼叫抽獎 API
        const response = await fetch('/api/draw', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });

        const data = await response.json();

        if (data.success) {
            const prize = data.prize;

            // 延遲顯示獎品（等方塊動畫完成）
            setTimeout(() => {
                // 更新獎品顯示
                prizeEmoji.textContent = prize.emoji;
                prizeName.textContent = prize.name;
                prizeRarity.textContent = rarityText[prize.rarity] || prize.rarity;
                prizeRarity.className = `prize-rarity ${prize.rarity}`;

                // 顯示獎品彈出
                prizePopup.classList.add('show');

                // 更新金幣計數
                totalDraws++;
                coinCount.textContent = totalDraws;

                // 添加到歷史紀錄
                addToHistory(prize);

                // 重置方塊
                setTimeout(() => {
                    questionBlock.classList.remove('hit');
                }, 500);

            }, 300);
        }
    } catch (error) {
        console.error('抽獎失敗:', error);
        alert('抽獎失敗，請再試一次！');
        questionBlock.classList.remove('hit');
    }

    // 重新啟用按鈕
    setTimeout(() => {
        isDrawing = false;
        drawButton.disabled = false;
    }, 1000);
}

// 添加到歷史紀錄
function addToHistory(prize) {
    // 移除空白提示
    const emptyHistory = historyList.querySelector('.empty-history');
    if (emptyHistory) {
        emptyHistory.remove();
    }

    // 建立歷史項目
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';

    const now = new Date();
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;

    historyItem.innerHTML = `
        <span class="history-emoji">${prize.emoji}</span>
        <div class="history-info">
            <span class="history-name">${prize.name}</span>
            <span class="history-time">${timeStr}</span>
        </div>
        <span class="prize-rarity ${prize.rarity}">${rarityText[prize.rarity]}</span>
    `;

    // 插入到最前面
    historyList.insertBefore(historyItem, historyList.firstChild);

    // 限制歷史紀錄數量
    while (historyList.children.length > 20) {
        historyList.removeChild(historyList.lastChild);
    }
}

// 事件監聽
drawButton.addEventListener('click', draw);
questionBlock.addEventListener('click', draw);

// 鍵盤支援（空白鍵抽獎）
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && !isDrawing) {
        e.preventDefault();
        draw();
    }
});

// 初始化顯示
prizePopup.classList.add('show');
prizeName.textContent = '按下方塊抽獎！';
prizeEmoji.textContent = '❓';
prizeRarity.textContent = '';
