from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from teamsync.models import Group
from teamsync.dao.github.organizations import get_team_members,\
    add_team_membership, remove_team_membership
from teamsync.dao.groups import get_group_members
from restclients.exceptions import DataFailureException
from logging import getLogger


logger = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):

        org_id = getattr(settings, 'GITHUB_ORGANIZATION')

        # Group-to-team mappings that need to be synced
        team_groups = Group.objects.get_team_lookup()

        for team_id in team_groups.keys():
            # The local membership of this team
            group_members = get_group_members(team_groups[team_id])

            # The existing membership of this team
            team_members = get_team_members(team_id)

            for user in [u for u in group_members if u not in team_members]:
                add_team_membership(team_id, member)
                logger.info('Added %s to team %s' % (user, team_id))

            for user in [u for u in team_members if u not in group_members]:
                remove_team_membership(team_id, member)
                logger.info('Removed %s from team %s' % (user, team_id))

            Group.objects.update_last_sync_date(team_id)
