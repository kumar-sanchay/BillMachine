from django.contrib import admin
from .models import UserModel, RecentActivities


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    list_filter = ['date_joined', 'active']


@admin.register(RecentActivities)
class RecentActivitiesAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'active']
    list_filter = ['active', 'created']