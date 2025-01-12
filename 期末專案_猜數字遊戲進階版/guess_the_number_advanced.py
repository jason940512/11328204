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
