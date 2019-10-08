from django.db import models
from math import floor, ceil
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

# Create your models here.
class RatePlan(models.Model):
    CATEGORY_CHOICE = (
        (0, '小型犬'),
        (1, '中型犬'),
        (2, '大型犬'),
        (3, '猫'),
    )
    DC_CHOICE = (
        (0, 'なし'),
        (1, '1vac'),
        (2, '2vac'),
        (3, '3vac'),
    )
    HS_CHOICE = (
        (0, '未加入'),
        (1, 'プラチナ年払い'),
        (2, 'スタンダード年払い'),
        (3, 'プラチナ月払い'),
        (4, 'スタンダード月払い'),
    )
    INSURANCE_CHOICE = (
        (0, '未加入'),
        (1, '100%年払い'),
        (2, '70%年払い'),
        (3, '100%月払い'),
        (4, '70%月払い'),
    )
    FOOD_CHOICE = (
        (0, 'なし'),
        (1, 'あり'),
    )
    HOME_CHOICE = (
        (0, 'なし'),
        (1, 'サークル無しセット'),
        (2, 'サークルセット（小）'),
        (3, 'サークルセット（大）'),
    )
    CARE_CHOICE = (
        (0, 'なし'),
        (1, '短毛用'),
        (2, '長毛用'),
    )
    LOAN_COMPANY_CHOICE = (
        ('一括', '一括'),
        ('PFクレジット', 'PFクレジット'),
        ('アプラス①', 'アプラス①'),
        ('アプラス②', 'アプラス②'),
        ('アプラス③', 'アプラス③'),
        ('PFS', 'PFS'),
        ('FLEX', 'FLEX'),
        ('セディナ', 'セディナ'),
        ('西京カード', '西京カード'),
        ('シティックス', 'シティックス'),
    )
    SUMMER_CHOICE = (
        (6, '6月'),
        (7, '7月'),
        (8, '8月'),
    )
    WINTER_CHOICE = (
        (12, '12月'),
        (1, '1月'),
    )

    pet_price = models.IntegerField('ペット代金', help_text='*税込み金額/半角数字で入力')
    other_price = models.IntegerField('その他購入代金', default=0)
    category = models.IntegerField('種別', choices=CATEGORY_CHOICE, default=0)
    dc_plan = models.IntegerField('ドクターズチェックP', help_text='*狂犬病接種の場合は3vacを選択', choices=DC_CHOICE, default=1)
    hs_plan = models.IntegerField('ほっとサポート', choices=HS_CHOICE, default=0)
    insurance_plan = models.IntegerField('ペット保険', choices=INSURANCE_CHOICE, default=0)
    insurance_discount = models.BooleanField('保険多頭割', help_text='*多頭割の場合はチェック', default=False)
    food_plan = models.IntegerField('ごはんセット', choices=FOOD_CHOICE, default=0)
    home_plan = models.IntegerField('おうちセット', choices=HOME_CHOICE, default=0)
    care_plan = models.IntegerField('しつけお手入れセット', choices=CARE_CHOICE, default=0)
    loan_company = models.CharField('支払方法', max_length=10, choices=LOAN_COMPANY_CHOICE, default='アプラス①')
    down_payment = models.IntegerField('頭金', default=0)
    bonus_setting = models.BooleanField('ボーナス支払設定', help_text='*ボーナス支払を設定する場合はチェック', default=False)
    bonus_payment = models.IntegerField('ボーナス加算額', help_text='*1000円単位で入力', default=0)
    bonus_s_month = models.IntegerField('ボーナス月（夏）', choices=SUMMER_CHOICE, default=6)
    bonus_w_month = models.IntegerField('ボーナス月（冬）', choices=WINTER_CHOICE, default=12)
    created_at = models.DateField('作成日', default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作成者')

    category_dict = ('小型犬', '中型犬', '大型犬', '猫',)
    sub_category_dict = ('犬', '犬', '犬', '猫')
    dc_dict = {
        '犬': (0, 58190, 68310, 79090),
        '猫': (0, 48840, 58960, 58960),
    }
    hs_r_dict = {
        '犬': 0.18,
        '猫': 0.15,
    }
    insurance_dict = {
        '小型犬': (0, 65020, 50280, 19550, 17000),
        '中型犬': (0, 77610, 59690, 23380, 20260),
        '大型犬': (0, 85320, 65450, 25720, 22280),
        '猫': (0, 53550, 41710, 16070, 14020),
    }
    insurance_dc_dict = {
        '小型犬': (0, 61880, 47980, 18680, 16340),
        '中型犬': (0, 73860, 56970, 22330, 19510),
        '大型犬': (0, 81200, 62470, 24580, 21440),
        '猫': (0, 50960, 39800, 15350, 13480),
    }
    insurance_m_dict = {
        '小型犬': (0, 0, 0, 5750, 4210),
        '中型犬': (0, 0, 0, 6860, 4980),
        '大型犬': (0, 0, 0, 7540, 5460),
        '猫': (0, 0, 0, 4740, 3500),
    }
    insurance_dc_m_dict = {
        '小型犬': (0, 0, 0, 5460, 3990),
        '中型犬': (0, 0, 0, 6510, 4730),
        '大型犬': (0, 0, 0, 7160, 5180),
        '猫': (0, 0, 0, 4500, 3320),
    }
    food_dict = {
        '犬': (0, 27500),
        '猫': (0, 18590),
    }
    home_dict = {
        '犬': (0, 20980, 39380, 61600),
        '猫': (0, 0, 36080, 43450),
    }
    care_dict = {
        '犬': (0, 19360, 20900),
        '猫': (0, 12870, 12870),
    }
    loan_dict = {
        'PFクレジット':
            {'回数':(1,2,3,5,6,10,12,15,18,20,24,30,36,42,48,54,60,72,84),
            '金利': (1.50,2.26,3.01,4.54,5.32,8.43,10.02,12.42,14.85,16.49,19.82,24.92,30.15,35.51,41.00,46.62,52.36,64.22,76.55),
            '支払日': 27,
            '開始月': 1,},
        'アプラス①':
            {'回数':(3,6,10,12,15,18,20,24,30,36,42,48,54,60,72,84),
            '金利': (0.00,0.00,0.00,8.16,10.20,12.20,13.60,16.30,20.40,24.50,28.60,32.60,36.70,40.80,49.00,57.10),
            '支払日': 27,
            '開始月': 1,},
        'アプラス②':
            {'回数':(3,6,10,12,15,18,20,24,30,36,42,48,54,60,72,84),
            '金利': (0.00,0.00,0.00,8.16,10.20,12.20,13.60,16.30,20.40,24.50,28.60,32.60,36.70,40.80,49.00,57.10),
            '支払日': 27,
            '開始月': 2,},
        'アプラス③':
            {'回数':(3,6,10,12,15,18,20,24,30,36,42,48,54,60,72,84),
            '金利': (0.00,0.00,0.00,8.16,10.20,12.20,13.60,16.30,20.40,24.50,28.60,32.60,36.70,40.80,49.00,57.10),
            '支払日': 27,
            '開始月': 3,},
        'PFS':
            {'回数':(1,3,6,10,12,15,18,20,24,30,36,42,48,54,60,72,84),
            '金利': (0.00,0.00,0.00,0.00,8.16,10.20,12.24,13.60,16.32,20.40,24.48,28.56,32.64,36.72,40.80,48.96,57.12),
            '支払日': 27,
            '開始月': 1,},
        'FLEX':
            {'回数':(3,10,12,15,18,20,24,36,48,60,72,84),
            '金利': (2.40,8.00,9.60,12.00,14.40,16.00,19.20,28.80,38.40,48.00,57.60,67.20),
            '支払日': 27,
            '開始月': 2,},
        'セディナ':
            {'回数':(1,2,3,5,8,10,12,15,18,20,24,30,36,42,48,54,60,72,84),
            '金利': (0.00,0.00,0.00,0.00,0.00,0.00,6.00,8.00,9.00,10.50,12.60,16.00,18.90,22.20,25.40,28.60,31.80,38.10,44.50),
            '支払日': 27,
            '開始月': 1,},
        '西京カード':
            {'回数':(1,2,3,5,10,12,15,18,20,24,30,36,42,48,54,60),
            '金利': (),
            '支払日': 6,
            '開始月': 2,},
        'シティックス':
            {'回数':(1,2,3,5,10,12,15,18,20,24,30,36,42,48,54,60),
            '金利': (),
            '支払日': 27,
            '開始月': 1,},
    }

    def __str__(self):
        return str(self.pet_price)

    """ドクターズチェック代金"""
    def dc_price(self, category, dc_plan):
        sub_category = RatePlan.sub_category_dict[category]
        dc_price = RatePlan.dc_dict[sub_category][dc_plan]
        return dc_price

    """ほっとサポート代金"""
    def hs_price(self, pet_price, category, hs_plan):
        hs_rate = RatePlan.hs_r_dict[RatePlan.sub_category_dict[category]]
        if pet_price <= 110000:
            hs_price = int(110000 * hs_rate)
            if hs_plan == 1:
                hs_price += 20000
            elif hs_plan == 3:
                hs_price = floor((hs_price + 20000) / 120) * 30
            elif hs_plan == 4:
                hs_price = floor(hs_price / 120) * 30
            else:
                hs_price = 0
        else:
            hs_price = int(pet_price * hs_rate)
            if hs_plan == 1:
                hs_price += 20000
            elif hs_plan == 3:
                hs_price = floor((hs_price + 20000) / 120) * 30
            elif hs_plan == 4:
                hs_price = floor(hs_price / 120) * 30
            else:
                hs_price = 0
        return hs_price

    """ほっとサポート月々支払額（月払い選択時のみ実行）"""
    def hs_m_price(self, hs_price):
        hs_m_price = int(hs_price / 3)
        return hs_m_price

    """保険代金"""
    def insurance_price(self, category, insurance_plan, insurance_discount):
        main_category = RatePlan.category_dict[category]
        if insurance_discount == False:
            insurance_price = RatePlan.insurance_dict[main_category][insurance_plan]
        elif insurance_discount == True:
            insurance_price = RatePlan.insurance_dc_dict[main_category][insurance_plan]
        return insurance_price

    """保険月々支払額（月払い選択時のみ実行）"""
    def insurance_m_price(self, category, insurance_plan, insurance_discount):
        main_category = RatePlan.category_dict[category]
        if insurance_discount == False:
            insurance_m_price = RatePlan.insurance_m_dict[main_category][insurance_plan]
        else:
            insurance_m_price = RatePlan.insurance_dc_m_dict[main_category][insurance_plan]
        return insurance_m_price

    """ごはんセット代金"""
    def food_price(self, category, food_plan):
        sub_category = RatePlan.sub_category_dict[category]
        food_price = RatePlan.food_dict[sub_category][food_plan]
        return food_price

    """おうちセット代金"""
    def home_price(self, category, home_plan):
        sub_category = RatePlan.sub_category_dict[category]
        home_price = RatePlan.home_dict[sub_category][home_plan]
        return home_price

    """しつけお手入れセット代金"""
    def care_price(self, category, care_plan):
        sub_category = RatePlan.sub_category_dict[category]
        care_price = RatePlan.care_dict[sub_category][care_plan]
        return care_price

    """用品セット割"""
    def set_discount(self, category, food_plan, home_plan, care_plan):
        sub_category = RatePlan.sub_category_dict[category]
        set_discount = 0
        if sub_category == '犬':
            if food_plan == 1:
                if care_plan == 1 or care_plan == 2:
                    if home_plan == 2:
                        set_discount = -6000
                    elif home_plan == 3:
                        set_discount = -10000
        return set_discount

    """トータル金額"""
    def total_price(self, pet_price, other_price, dc_price, hs_price, insurance_price, food_price, home_price, care_price, set_discount) :
        total_price = pet_price + other_price + dc_price + hs_price + insurance_price + food_price + home_price + care_price + set_discount
        return total_price

    """分割元金"""
    def capital(self, total_price, down_payment):
        capital = total_price - down_payment
        return capital

    """手数料リスト作成"""
    def ratefee_list(self,capital ,rate_list):
        ratefee_list = []
        count = len(rate_list)
        for c in range(count):
            rate = rate_list[c]
            ratefee = int(capital * rate / 100)
            ratefee_list.append(ratefee)
        return ratefee_list

    """分割支払金総額リスト作成"""
    def totalsplit_list(self, capital, ratefee_list):
        totalsplit_list = []
        for ratefee in ratefee_list:
            totalsplit = capital + ratefee
            totalsplit_list.append(totalsplit)
        return totalsplit_list

    """月々支払金リスト"""
    def splitmonth_list(self,totalsplit_list, number_list, b_total_list):
        splitmonth_list = []
        for number, ts, bt in zip(number_list, totalsplit_list, b_total_list):
            set_list = []
            ts -= bt
            split2 = int((ts / 100) / number) * 100
            split1 = ts - (split2 * (number - 1))
            if number == 1:
                split2 = ts
                split1 = 0
            set_list.append(split2)
            set_list.append(split1)
            splitmonth_list.append(set_list)
        return splitmonth_list

    """支払開始日"""
    def start_date(self, created_at, month, day):
        editdate = date(created_at.year, created_at.month, day)
        start_date = editdate + relativedelta(months=month)
        return start_date

    """支払完了日リスト"""
    def enddate_list(self, start_date, number_list):
        enddate_list = []
        for n in number_list:
            n -= 1
            enddate = start_date + relativedelta(months=n)
            enddate = enddate.strftime('%Y/%m')
            enddate_list.append(enddate)
        return enddate_list

    """ボーナス適用回数リスト"""
    def b_count_list(self, start_date, number_list):
        b_count_list = []
        for n in number_list:
            b_count = 0
            for c in range(n):
                check_date = start_date + relativedelta(months=c)
                if check_date.month ==  self.bonus_s_month or check_date.month == self.bonus_w_month:
                    b_count += 1
            b_count_list.append(b_count)
        return b_count_list

    """ボーナス総支払額リスト"""
    def b_total_list(self, b_count_list):
        b_total_list = []
        for c in b_count_list:
            if self.bonus_setting == False:
                b_total = 0
            else:
                b_total = c * self.bonus_payment
            b_total_list.append(b_total)
        return b_total_list

    """ボーナス比率リスト"""
    def b_ratio_list(self, b_total_list, capital):
        b_ratio_list = []
        for bt in b_total_list:
            if bt == 0:
                b_ratio = str(0) + '%'
            else:
                b_ratio = str(ceil(bt / capital * 100)) + '%'
            b_ratio_list.append(b_ratio)
        return b_ratio_list
