from django.forms import ModelForm
from .models import RatePlan


class RatePlanForm(ModelForm):
    class Meta:
        model = RatePlan
        fields = (
            'pet_price', 'other_price', 'category', 'dc_plan', 'hs_plan',
            'insurance_plan', 'insurance_discount', 'food_plan', 'home_plan',
            'care_plan', 'loan_company', 'down_payment', 'bonus_setting',
            'bonus_payment', 'bonus_s_month', 'bonus_w_month')
