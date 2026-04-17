import random

choices = {1: "🥢棒子", 2: "🐯老虎", 3: "🐓公雞", 4: "🐛蟲子"}
win_map = {1: 2, 2: 3, 3: 4, 4: 1}

def play_game():
    player_win = 0
    computer_win = 0
    tie_count = 0

    while True:
        try:
            user_choice = int(input("請選擇 (0.離開 1.🥢棒子 2.🐯老虎 3.🐓公雞 4.🐛蟲子): "))
            
            if user_choice == 0:
                total_rounds = player_win + computer_win + tie_count
                print("\n📊 遊戲結束，戰績統計：")
                print(f"🎮 總共猜拳 {total_rounds} 次")
                print(f"✅ 你贏了 {player_win} 次")
                print(f"💻 電腦贏了 {computer_win} 次")
                print(f"🤝 平手 {tie_count} 次")
                print("👋 謝謝遊玩！")
                break
            
            if user_choice not in choices:
                print("⚠️ 輸入錯誤，請選擇 0-4")
                continue
        except ValueError:
            print("⚠️ 請輸入數字 0-4")
            continue

        computer_choice = random.randint(1, 4)
        print(f"你選擇: {choices[user_choice]}，電腦選擇: {choices[computer_choice]}")

        if user_choice == computer_choice:
            print("🤝 平手！")
            tie_count += 1
        elif win_map[user_choice] == computer_choice:
            print("🎉 你贏了！")
            player_win += 1
        else:
            print("💻 電腦贏了！")
            computer_win += 1

play_game()