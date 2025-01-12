# 猜數字遊戲進階版

## 專案簡介
本專案是一款簡易且有趣的猜數字遊戲。玩家需要根據提示選擇遊戲難度，並在限定次數內猜中隨機生成的目標數字。該專案結合了難度選擇、排行榜記錄等功能，並提供詳細的遊戲過程解說和錯誤處理，幫助玩家體驗更佳。

---

## 專案功能
1. **難度選擇功能**：
   - **簡單模式**：數字範圍 1~50，挑戰次數 10。
   - **中等模式**：數字範圍 1~100，挑戰次數 7。
   - **困難模式**：數字範圍 1~200，挑戰次數 5。
   - 每種難度均顯示清晰的數字範圍及可用挑戰次數。

2. **排行榜功能**：
   - 玩家輸入名字後，其最高分數會被記錄。
   - 排行榜資料存儲於 JSON 檔案中，便於讀取與更新。

3. **分數計算**：
   - 根據剩餘挑戰次數計算得分，猜中越早得分越高。
   - 若挑戰次數耗盡，該次遊戲得分記為 0。

4. **錯誤處理與用戶體驗**：
   - 玩家輸入非數字時，提供友好的提示訊息。
   - 主選單和難度選擇界面設計直觀，易於操作。

---

## 程式碼

```Python
import random
import json
import os

SCORES_FILE = "scores.json"

def load_scores():
    """從JSON文件中下載排行榜數據"""
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as file:
            return json.load(file)
    return {}

def save_scores(scores):
    """保存排行榜數據到JSON文件"""
    with open(SCORES_FILE, "w") as file:
        json.dump(scores, file)

def get_difficulty():
    """讓玩家選擇遊戲難度，返回對應範圍和挑戰次數"""
    print("\n請選擇遊戲難度:")
    options = {
        "1": (1, 50,  5, "簡單"),
        "2": (1, 100, 7, "中等"),
        "3": (1, 200, 10, "困難")
    }
    for key, (start, end, attempts, level) in options.items():
        print(f"{key}. {level} (範圍: {start} 到 {end}, {attempts} 次機會)")
    
    while True:
        choice = input("請選擇難度 (1/2/3): ").strip()
        if choice in options:
            start, end, max_attempts, level = options[choice]
            print(f"\n你選擇了【{level}】，挑戰範圍是 {start} 到 {end}，共有 {max_attempts} 次機會。\n")
            return start, end, max_attempts
        print("無效的選擇，請重新輸入!")

def play_game():
    """執行一次遊戲挑戰，並返回得分結算"""
    print("歡迎來到進階版猜數字遊戲!")
    start, end, max_attempts = get_difficulty()
    target = random.randint(start, end)
    attempts = 0
    
    print(f"我選擇了一個 {start} 到 {end} 的數字，你有 {max_attempts} 次機會來猜中它!")

    while attempts < max_attempts:
        try:
            guess = input(f"第 {attempts + 1}/{max_attempts} 次猜測，請輸入數字: ").strip()
            if not guess.isdigit():
                print("請輸入一個有效的數字!")
                continue

            guess = int(guess)
            attempts += 1

            if guess < target:
                print("太小了!")
            elif guess > target:
                print("太大了!")
            else:
                print(f"恭喜你，猜中了! 答案是 {target}。")
                return max_attempts - attempts + 1  # 返回剩餘次數作為得分
        except ValueError:
            print("發生錯誤，請輸入有效的數字!")
    
    print(f"很遺憾，次數用完了! 答案是 {target}。")
    return 0  # 若挑戰失敗，返回 0 分

def update_scores(name, score):
    """更新排行榜數據"""
    scores = load_scores()
    if name in scores:
        scores[name] = max(scores[name], score)  # 保留最高分
    else:
        scores[name] = score
    save_scores(scores)

def display_scores():
    """顯示排行榜"""
    print("\n排行榜:")
    scores = load_scores()
    if not scores:
        print("目前沒有記錄!")
        return
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for rank, (name, score) in enumerate(sorted_scores, start=1):
        print(f"{rank}. {name}: {score} 分")

def main():
    """主程式入口"""
    while True:
        print("\n主選單:")
        print("1. 開始遊戲")
        print("2. 查看排行榜")
        print("3. 離開")
        choice = input("請選擇 (1/2/3): ").strip()
        
        if choice == "1":
            name = input("請輸入你的名字: ").strip()
            if not name:
                print("名字不能為空，請重新輸入!")
                continue
            score = play_game()
            print(f"你的得分: {score}")
            update_scores(name, score)
        elif choice == "2":
            display_scores()
        elif choice == "3":
            print("感謝遊玩，再見!")
            break
        else:
            print("無效選擇，請重新輸入!")

if __name__ == "__main__":
    main()
```
## 使用指引
- 在VSC或其他終端選擇執行後，根據主選單提示選擇操作：
   - `1`：開始遊戲，選擇難度並進行猜數字挑戰。
   - `2`：查看排行榜，顯示玩家最高分數(若顯示「目前沒有紀錄!」則請先輸入`1`開始遊戲)。
   - `3`：退出遊戲(程式碼停止執行)。
## 實機遊玩畫面
1. ![image](https://github.com/jason940512/11328204/blob/main/%E6%9C%9F%E6%9C%AB%E5%B0%88%E6%A1%88_%E7%8C%9C%E6%95%B8%E5%AD%97%E9%81%8A%E6%88%B2%E9%80%B2%E9%9A%8E%E7%89%88/%E8%9E%A2%E5%B9%95%E6%93%B7%E5%8F%96%E7%95%AB%E9%9D%A2%202025-01-13%20012911.png)
2. ![image](https://github.com/jason940512/11328204/blob/main/%E6%9C%9F%E6%9C%AB%E5%B0%88%E6%A1%88_%E7%8C%9C%E6%95%B8%E5%AD%97%E9%81%8A%E6%88%B2%E9%80%B2%E9%9A%8E%E7%89%88/%E8%9E%A2%E5%B9%95%E6%93%B7%E5%8F%96%E7%95%AB%E9%9D%A2%202025-01-13%20012821.png)
3. ![image]()
4. ![image]()
## 學習歷程
1. **Python基礎運用**：
   - 熟悉 Python 的基礎語法，例如 `input()` 函數、條件語句、迴圈等。
   - 使用 `random.randint()` 函數生成隨機數字，學習隨機模組的基本操作。
   - 利用`ChatGPT`進行程式碼整合、除錯、改良，並從中了解各行程式碼的意思及目的。
2. **檔案操作與資料存儲**：
   - 學習 `ChatGPT`提供之`json`模組讀寫排行榜數據，以實現排行榜計分。
   - 學習檔案操作相關函數，例如 `open()` 和 `os.path.exists()`。
3. **遊戲邏輯設計**：
     - 設計合理的遊戲流程，包括主選單、難度選擇、猜測過程等。
     - 新增除錯，提醒確保玩家輸入無效關鍵字時不會導致程式輸出結果錯誤。
4. **玩家體驗改進**：
     - 增加難度選擇時的詳細範圍和次數提示，以確保玩家輸入數字與難度範圍相符。
     - 在每次輸入後提供即時回饋（例如數字過大或過小）。
     - 設計排行榜功能，讓小遊戲不僅僅侷限於單機遊玩，也能享受與其他玩家對抗的快感。
## 未來可改進之方向
   - 利用 `PyQt6` 等程式開發UI介面，使操作更為方便直觀。
   - 增加限時模式，提升遊戲的刺激感。
