import os
import uuid
import yaml
import shutil
import subprocess
import gevent

from onghub.git import Git


class Job(object):
    def __init__(self, app, project, event):
        self.app = app
        self.project = project
        self.id = str(uuid.uuid4())
        self.path = os.path.join(project.path, self.id)
        self.event = event
        self._config = None
    
    @property
    def config_path(self):
        return os.path.join(self.repo_path, '.onghub.yml')

    @property
    def logfile_path(self):
        return os.path.join(self.path, 'log')
    
    @property
    def repo_path(self):
        return os.path.join(self.path, 'repo')
    
    @property
    def config(self):
        if self._config is None:
            if not os.path.exists(self.config_path):
                self._config = {}
            else:
                with open(self.config_path, 'r') as f:
                    self._config = yaml.load(f)
        return self._config
    
    def start(self):
        return self.app.spawn(self.run)
    
    def run(self):
        print "running job %s for %s" % (self.id, self.project.repo_slug)
        git = Git(self.repo_path)
        git.clone(self.project.git_url, depth=1)
        print self.config
        script = self.config.get('script')
        with open(self.logfile_path, 'w') as logfile:
            for command in script:
                subprocess.call(command, stdout=logfile, stderr=subprocess.STDOUT, shell=True)

    def cleanup(self):
        shutil.rmtree(self.path)


    