from django.contrib import admin
from .models import SystemSetting, FiscalYear

@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'setting_type', 'is_active')
    list_filter = ('setting_type', 'is_active')
    search_fields = ('key', 'name')

@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date', 'is_current')
    list_editable = ('is_current',)
    ordering = ('-year',)