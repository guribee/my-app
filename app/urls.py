from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'app'

urlpatterns = [
    path('top/', views.index, name='index'),
    # path('history/<str:user_name>/', views.history, name='history'),
    path('history/<str:user_name>/', views.PlanList.as_view(), name='history'),
    path('new_plan/', views.new_plan, name='new_plan'),
    path('plan/edit/<int:plan_id>/', views.new_plan, name='edit'),
    path('plan/result/<int:plan_id>/', views.result, name='result'),
    path('delete/<int:plan_id>/', views.delete, name='delete'),
    path('document/', views.document, name='document'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
