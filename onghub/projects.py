import os
import re
import shutil
import gevent

from onghub.jobs import Job


REPO_SLUG_RE = re.compile(r'^\w+/\w+$')


class Project(object):
    def __init__(self, app, repo_slug):
        if not REPO_SLUG_RE.match(repo_slug):
            raise ValueError('invalid repo slug: %r' % repo_slug)
        self.app = app
        self.repo_slug = repo_slug
        self.path = os.path.join(self.app.job_dir, repo_slug)
    
    @property
    def key(self):
        return self.app.sign(self.repo_slug)

    @property
    def hook_url(self):
        return self.app.build_url('/hooks/%s' % self.key)

    def trigger(self, event=None):
        job = Job(self.app, self, event)
        job.start()
    
    @property
    def git_url(self):
        return 'git@github.com:%s.git' % self.repo_slug
    
    def delete(self):
        shutil.rmtree(self.path)
