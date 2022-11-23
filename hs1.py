def checkNujin1(usage, high, mid):
    try:
        total = 0
        # 기본요금
        if usage > high:
            basic = 7300
        elif usage > mid:
            basic = 1600
        else:
            basic = 910

        # 전력요금
        tmp = usage
        if tmp > high:
            total += 280.5 * (usage - high)
            total += 187.8 * (high - mid)
            total += 93.2 * mid

        elif mid < usage <= high:
            total += 187.8 * (usage - mid)
            total += 93.2 * (high - mid)

        else:
            total += 93.2 * usage
            # print(3, total)

        total += basic
        return total
    except:
        total =0 
        return total



'''
while True:
    usage = int(input("이번달 전기 사용량을 입력하세요 : "))

    print("하계 전력요금 이번달 전기요금은 ", checkNujin1(usage, 450, 300), "입니다.")
    print("기타계절 전력요금 이번달 전기요금은 ", checkNujin1(usage, 400, 200), "입니다.")
'''