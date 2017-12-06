from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from teamsync.dao.github.organizations import get_members_for_org
from teamsync.models import User


class Command(BaseCommand):
    help = 'Adds users from GitHub'

    def handle(self, *args, **options):
        org_id = getattr(settings, 'GITHUB_ORGANIZATION')

        for username in get_members_for_org(org_id):
            try:
                user = User.objects.get(github_username=username)
            except User.DoesNotExist:
                user = User(github_username=username)
                user.save()
