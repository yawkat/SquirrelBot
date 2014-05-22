import git_shared
import gitlab

class Gitlab(git_shared.GitModule):
    def __init__(self, id, on, url, name, project, auth = None):
        super(Gitlab, self).__init__(id, on, name)
        self.project = project

        self.git = gitlab.Gitlab(url, token=auth)
        self.known = None

    def _poll(self):
        commits = self.git.listrepositorycommits(self.project)
        commits.reverse()
        for commit in commits:
            self._commit(commit["id"], commit["title"], commit["author_name"])