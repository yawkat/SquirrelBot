import git_shared
import github

class Github(git_shared.GitModule):
    def __init__(self, id, on, name, project, auth = None):
        super(Github, self).__init__(id, on, name, rate=10)
        self.git = github.Github(login_or_token=auth)
        self.repo = self.git.get_repo(project)

    def _poll(self):
        commits = self.repo.get_commits().get_page(0)
        commits.reverse()
        for commit in commits:
            self._commit(commit.sha, commit.commit.message, commit.committer.name)