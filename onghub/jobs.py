import os
import uuid
import yaml
import shutil
import gevent

from onghub.git import Git


class Job(object):
    def __init__(self, app, project):
        self.app = app
        self.project = project
        self.path = os.path.join(self.app.job_dir, self.project.repo_slug, str(uuid.uuid4()))
        self._config = None
    
    @property
    def config_file_path(self):
        return os.path.join(self.path, '.travis.yml')
    
    @property
    def config(self):
        if self._config is None:
            if not os.path.exists(self.config_file_path):
                self._config = {}
            else:
                with open(self.config_file_path, 'r') as f:
                    self._config = yaml.load(f)
        return self._config
    
    def start(self):
        return self.app.spawn(self.run)
    
    def run(self):
        print "running job for %s" % self.project
        git = Git(self.path)
        git.clone(self.project.git_url, depth=1)
        print self.config

    def cleanup(self):
        shutil.rmtree(self.path)


    