import gevent.monkey
gevent.monkey.patch_all()

import yaml
import sys
import logging
import argparse

from onghub.app import Onghub


def create_app():
    with open('onghub.yml', 'r') as f:
        config = yaml.load(f)
    return Onghub(config)


def run_hook(app, args):
    project = app.get_project(args.repo_slug)
    print project.hook_url


def run_trigger(app, args):
    project = app.get_project(args.repo_slug)
    project.trigger()


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
    
    app = create_app()
    
    args = parser.parse_args()
    args.command(app, args)
    
    app.join()
    

if __name__ == '__main__':
    main()