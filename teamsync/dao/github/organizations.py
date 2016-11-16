from teamsync.dao.github import GitHub_DAO as github


def get_members_for_org(org_id):
    url = '/orgs/%s/members' % org_id
    return github().getURL(url)


def get_teams_for_org(org_id):
    url = '/orgs/%s/teams' % org_id
    return github().getURL(url)


def get_team_members(team_id):
    url = '/teams/%s/members' % team_id
    members = []
    for member in github().getURL(url):
        members.append(member.login)
    return members


def add_team_membership(team_id, username):
    url = '/teams/%s/memberships/%s' % (team_id, username)
    return github().putURL(url)


def remove_team_membership(team_id, username):
    url = '/teams/%s/memberships/%s' % (team_id, username)
    return github().deleteURL(url)
