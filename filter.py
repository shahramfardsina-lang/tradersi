def filter_coins(coins):

    # فعلاً فقط محدودیت تعداد
    # مرحله بعد امتیاز اولیه اضافه می‌کنیم

    max_coins = 20

    if len(coins) > max_coins:

        return coins[:max_coins]


    return coins