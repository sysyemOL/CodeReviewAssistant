def calculate_sum(numbers):
    """计算列表中数字的总和"""
    total = 0
    for num in numbers:
        total += num
    return total

def main():
    # 测试代码
    numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(numbers)
    print(f"总和为: {result}")

if __name__ == "__main__":
    main()

