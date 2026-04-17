# 從1加到100的程式
# 這個檔案包含三種計算從1加到100總和的方法：
# 1. 使用for迴圈一個一個加總
# 2. 使用等差級數的數學公式
# 3. 使用Python內建sum函數與range
# 並支援直接執行時的主程式，印出三種方法的結果與檢查結果是否一致



def sum_1_to_100():
    """計算從1加到100的總和"""
    total = 0
    for i in range(1, 101):  # range(1, 101) 包含1到100
        total += i
    return total

def sum_1_to_100_formula():
    """使用數學公式計算從1加到100的總和"""
    # 等差數列求和公式: n * (n + 1) / 2
    n = 100
    return n * (n + 1) // 2

def sum_1_to_100_builtin():
    """使用Python內建函數計算從1加到100的總和"""
    return sum(range(1, 101))

if __name__ == "__main__":
    # 方法1: 使用迴圈
    result1 = sum_1_to_100()
    print(f"使用迴圈計算: 1+2+3+...+100 = {result1}")

    # 方法2: 使用數學公式
    result2 = sum_1_to_100_formula()
    print(f"使用數學公式計算: 1+2+3+...+100 = {result2}")

    # 方法3: 使用Python內建函數
    result3 = sum_1_to_100_builtin()
    print(f"使用內建函數計算: 1+2+3+...+100 = {result3}")

    # 驗證結果是否一致
    print(f"\n所有方法的結果都相同: {result1 == result2 == result3}")

    # 顯示計算過程（可選）
    print("\n計算過程:")
    for i in range(1, 11):  # 只顯示前10個數字
        print(f"{i} + ", end="")
    print("... + 100")
