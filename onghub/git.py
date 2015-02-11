import subprocess
import shutil
import os


class Git(object):
    def __init__(self, path):
        self.path = path
    
    def _run(self, cmd, cwd=None):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd or self.path)
        stdout, stderr = popen.communicate()
        return stdout
    
    def rm(self):
        shutil.rmtree(self.path)

    def clone(self, url, depth=None):
        if os.path.exists(self.path):
            self.rm()
        dirname = os.path.dirname(self.path)
        basename = os.path.basename(self.path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        options = []
        if depth:
            options += ['--depth', str(depth)]
        return self._run(['git', 'clone'] + options + [url, basename], cwd=dirname)
    
    def head(self):
        return self._run(['git', 'rev-parse', 'HEAD'])
