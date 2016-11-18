from django.db import models
from django.core.cache import cache
from django.utils.timezone import utc
from datetime import datetime


class UserManager(models.Manager):
    def get_github_username(self, group_member_name):
        """
        Return the github_username for the passed group_member_name.
        """
        lookup = cache.get_or_set(
            'group_member_lookup',
            dict((m, u) for m, u in super(UserManager, self).get_queryset(
                ).exclude(group_member_name__isnull=True).values_list(
                    'group_member_name', 'github_username')),
            60*5)
        return lookup.get(group_member_name, None)


class User(models.Model):
    """
    Maps local group members to github users.
    """
    group_member_name = models.CharField(max_length=64, null=True, unique=True)
    github_username = models.CharField(max_length=64, unique=True)
    added_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    class Meta:
        db_table = 'teamsync_user'


class GroupManager(models.Manager):
    def get_team_lookup(self):
        mapping = {}
        for g, t in super(GroupManager, self).get_queryset().exclude(
                group_id__isnull=True).values_list('group_id', 'team_id'):
            try:
                mapping[t].append(g)
            except Exception:
                mapping[t] = [g]
        return mapping

    def update_last_sync_date(self, team_id):
        super(GroupManager, self).get_queryset().filter(
                team_id=team_id
            ).update(
                last_sync_date=datetime.utcnow().replace(tzinfo=utc))


class Group(models.Model):
    """
    Maps local groups to github teams.
    """
    group_id = models.CharField(max_length=128, null=True)
    team_id = models.CharField(max_length=16)
    team_name = models.CharField(max_length=128, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    last_sync_date = models.DateTimeField(null=True)

    objects = GroupManager()

    class Meta:
        db_table = 'teamsync_group'
        unique_together = ('group_id', 'team_id')
