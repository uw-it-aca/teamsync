from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from teamsync.models import Group
from teamsync.dao.github.organizations import (
    get_teams_for_org, get_team_members, add_team_membership,
    remove_team_membership)
from teamsync.dao.groups import get_group_members
from restclients.exceptions import DataFailureException
from logging import getLogger


logger = getLogger(__name__)


class Command(BaseCommand):
    help = 'Reconcile GitHub teams with local groups'

    def add_arguments(self, parser):
        parser.add_argument('--commit', action='store_true', dest='commit',
                            default=False, help='Actually update GitHub teams')

    def handle(self, *args, **options):
        is_commit = options.get('commit')
        if not is_commit:
            print('Not committing changes to GitHub, use --commit')

        org_id = getattr(settings, 'GITHUB_ORGANIZATION')

        # Group-to-team mappings that need to be synced
        team_groups = Group.objects.get_team_lookup()

        # Existing teams in GitHub
        for team in get_teams_for_org(org_id):
            Group.objects.filter(team_id=team.get('id')).update(
                team_name=team.get('name'))

        for team_id in team_groups.keys():
            # The local membership of this team
            group_members = get_group_members(team_groups[team_id])

            # The existing membership of this team
            team_members = get_team_members(team_id)

            for user in [u for u in group_members if u not in team_members]:
                msg = 'Added %s to team %s' % (user, team_id)
                if is_commit:
                    add_team_membership(team_id, member)
                    logger.info(msg)
                else:
                    print(msg)

            for user in [u for u in team_members if u not in group_members]:
                msg = 'Removed %s from team %s' % (user, team_id)
                if is_commit:
                    remove_team_membership(team_id, member)
                    logger.info(msg)
                else:
                    print(msg)

            if is_commit:
                Group.objects.update_last_sync_date(team_id)
