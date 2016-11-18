from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from teamsync.dao.github.organizations import get_teams_for_org
from teamsync.models import Group
from restclients.exceptions import DataFailureException


class Command(BaseCommand):
    help = 'Adds teams from GitHub'

    def handle(self, *args, **options):
        org_id = getattr(settings, 'GITHUB_ORGANIZATION')

        for team in get_teams_for_org(org_id):
            try:
                group = Group.objects.get(team_id=team.get('id'))
            except Group.DoesNotExist:
                group = Group(team_id=team.get('id'))

            group.team_name = team.get('name')
            group.save()
