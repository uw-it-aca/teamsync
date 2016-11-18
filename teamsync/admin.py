from django.contrib import admin
from teamsync.models import User, Group


class UserAdmin(admin.ModelAdmin):
    list_display = ('group_member_name', 'github_username', 'added_date')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'team_id', 'team_name', 'added_date',
                    'last_sync_date')
    fields = ('group_id', 'team_id')


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
