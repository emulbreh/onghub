import gevent.monkey
gevent.monkey.patch_all()

import functools
import yaml
import sys
import logging
import argparse

from onghub.app import Onghub


def create_app():
    with open('onghub.yml', 'r') as f:
        config = yaml.load(f)
    return Onghub(config)


def project_command(func):
    @functools.wraps(func)
    def decorated(app, args):
        project = app.get_project(args.repo_slug)
        return func(app, project, args)
    return decorated


@project_command
def run_hook(app, project, args):
    print project.hook_url


@project_command
def run_trigger(app, project, args):
    project.trigger()


@project_command
def run_delete(app, project, args):
    project.delete()


def main():
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='')

    hook_parser = subparsers.add_parser('hook')
    hook_parser.add_argument('repo_slug')
    hook_parser.set_defaults(command=run_hook)
    
    trigger_parser = subparsers.add_parser('trigger')
    trigger_parser.add_argument('repo_slug')
    trigger_parser.set_defaults(command=run_trigger)
    
    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('repo_slug')
    delete_parser.set_defaults(command=run_delete)
    
    app = create_app()
    
    args = parser.parse_args()
    args.command(app, args)
    
    app.join()
    

if __name__ == '__main__':
    main()