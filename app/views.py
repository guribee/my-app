from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView
from .models import RatePlan
from .forms import RatePlanForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
    context = {
    }
    return render(request, 'app/index.html')

@login_required
def new_plan(request, plan_id=None):
    if plan_id:
        plan = get_object_or_404(RatePlan, pk=plan_id)
    else:
        plan = RatePlan()

    if request.method == 'POST':
        form = RatePlanForm(request.POST, instance=plan)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            messages.info(request, f'ID:{plan.id}で保存されました。履歴から操作可能です。')
            return redirect('app:result', plan_id=plan.id)
    else:
        form = RatePlanForm(instance=plan)
        context = {
            'form': form,
            'plan': plan,
            }
    return render(request, 'app/new_plan.html', context)

@login_required
def result(request, plan_id):
    plan = get_object_or_404(RatePlan, pk=plan_id)
    dc_price = plan.dc_price(plan.category, plan.dc_plan)
    hs_price = plan.hs_price(plan.pet_price, plan.category, plan.hs_plan)
    hs_m_price = 0
    if plan.hs_plan == 3 or plan.hs_plan == 4:
        hs_m_price = plan.hs_m_price(hs_price)
    insurance_price = plan.insurance_price(plan.category, plan.insurance_plan, plan.insurance_discount)
    insurance_m_price = 0
    if plan.insurance_plan == 3 or plan.insurance_plan == 4:
        insurance_m_price = plan.insurance_m_price(plan.category, plan.insurance_plan, plan.insurance_discount)
    food_price = plan.food_price(plan.category, plan.food_plan)
    home_price = plan.home_price(plan.category, plan.home_plan)
    care_price = plan.care_price(plan.category, plan.care_plan)
    set_discount = plan.set_discount(plan.category, plan.food_plan, plan.home_plan, plan.care_plan)
    total_price = plan.total_price(plan.pet_price, plan.other_price, dc_price, hs_price, insurance_price, food_price, home_price, care_price, set_discount)
    capital = plan.capital(total_price, plan.down_payment)
    number_list = RatePlan.loan_dict[plan.loan_company]['回数']
    ratefee_list = plan.ratefee_list(capital, RatePlan.loan_dict[plan.loan_company]['金利'])
    totalsplit_list = plan.totalsplit_list(capital, ratefee_list)
    start_date = plan.start_date(plan.created_at, RatePlan.loan_dict[plan.loan_company]['開始月'], RatePlan.loan_dict[plan.loan_company]['支払日'])
    b_count_list = plan.b_count_list(start_date, number_list)
    b_total_list = plan.b_total_list(b_count_list)
    b_ratio_list = plan.b_ratio_list(b_total_list, capital)
    splitmonth_list = plan.splitmonth_list(totalsplit_list, number_list, b_total_list)
    enddate_list = plan.enddate_list(start_date, number_list)
    simulation_list = []
    if plan.bonus_setting == False:
        for n, sm, ts, rf, ed in zip(number_list, splitmonth_list, totalsplit_list, ratefee_list, enddate_list):
            simulation_list.append(n)
            simulation_list.append(sm)
            simulation_list.append(ts)
            simulation_list.append(rf)
            simulation_list.append(ed)
            simulation_list.append('改行')
    else:
        for n, sm, ts, rf, ed, br in zip(number_list, splitmonth_list, totalsplit_list, ratefee_list, enddate_list, b_ratio_list):
            simulation_list.append(n)
            simulation_list.append(sm)
            simulation_list.append(ts)
            simulation_list.append(rf)
            simulation_list.append(ed)
            simulation_list.append(br)
            simulation_list.append('改行')
    context = {
        'plan': plan,
        'pet_price': plan.pet_price,
        'other_price': plan.other_price,
        'dc_price': dc_price,
        'hs_price': hs_price,
        'insurance_price': insurance_price,
        'insurance_discount' : plan.insurance_discount,
        'food_price': food_price,
        'home_price': home_price,
        'care_price': care_price,
        'set_discount': set_discount,
        'hs_m_price': hs_m_price,
        'insurance_m_price': insurance_m_price,
        'total_price': total_price,
        'down_payment': plan.down_payment,
        'capital': capital,
        'start_date': start_date,
        'simulation_list': simulation_list,
        }
    return render(request, 'app/result.html', context)

@require_POST
@login_required
def delete(request, plan_id):
    plan = get_object_or_404(RatePlan, pk=plan_id)
    user = get_object_or_404(User, username=plan.user.username)
    plan.delete()
    return redirect('app:history', user_name=user.username)

class PlanList(ListView):
    context_object_name = 'plans'
    template_name = 'app/history.html'
    paginate_by = 10

    def get(self, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['user_name'])
        plans = user.rateplan_set.all().order_by('-pk')
        self.object_list = plans
        context = self.get_context_data(object_list=self.object_list, user=user)
        return self.render_to_response(context)

# @login_required
# def history(request, user_name):
#     user = get_object_or_404(User, username=user_name)
#     plans = user.rateplan_set.all().order_by('-pk')
#     context = {
#         'plans': plans
#     }
#     return render(request, 'app/history.html', context)

@login_required
def document(request):
    return render(request, 'app/document.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(username=input_username, password=input_password)
            if new_user is not None:
                login(request, new_user)
                return redirect('app:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'app/signup.html', context)
