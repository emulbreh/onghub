import logging
import gevent

from itsdangerous import Signer

from onghub.projects import Project
from onghub.server import create_wsgi_app


logger = logging.getLogger(__name__)


class Onghub(object):
    def __init__(self, config):
        self.config = config
        self.signer = Signer(config['secret'])
        self.wsgi_app = create_wsgi_app(self)
        self.jobs = []
    
    def get_project(self, repo_slug):
        return Project(self, repo_slug)

    def sign(self, value):
        return self.signer.sign(value)
    
    def unsign(self, value):
        return self.signer.unsign(value)

    def build_url(self, path):
        return self.config.get('root_url', '') + path
    
    @property
    def job_dir(self):
        return self.config.get('job_dir', '_jobs')
    
    def spawn(self, func, *args, **kwargs):
        greenlet = gevent.spawn(func, *args, **kwargs)
        self.jobs.append(greenlet)
        return greenlet
    
    def join(self):
        gevent.joinall(self.jobs)