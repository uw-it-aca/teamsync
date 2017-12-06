from uw_gws import GWS
from teamsync.models import User


def get_group_members(group_ids):
    """
    Returns a list of github usernames for the passed list of group_ids,
    limited to group members present in teamsync.models.User.
    """
    gws = GWS()
    members = {}
    for group_id in group_ids:
        for member in gws.get_effective_members(group_id):
            username = User.objects.get_github_username(member.name)
            if username is not None:
                members[username] = True
    return members.keys()
