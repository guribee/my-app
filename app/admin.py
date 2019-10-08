from django.contrib import admin
from .models import RatePlan

# Register your models here.
class RatePlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'created_at')

admin.site.register(RatePlan, RatePlanAdmin)
