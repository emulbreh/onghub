import logging

from werkzeug.routing import Map, Rule
from werkzeug.exceptions import MethodNotAllowed, HTTPException
from werkzeug.wrappers import Request, Response

from onghub import jobs


http_methods = ('get', 'post', 'head', 'options', 'put', 'delete')

logger = logging.getLogger(__name__)


class Endpoint(object):
    def __init__(self, app):
        self.app = app

    @property
    def allowed_methods(self):
        return [method for method in http_methods if callable(getattr(self, method, None))]

    def dispatch(self, request, args):
        method = request.method.lower()
        if method not in http_methods:
            raise MethodNotAllowed(self.allowed_methods)
        try:
            func = getattr(self, method)
        except AttributeError:
            raise MethodNotAllowed(self.allowed_methods)
        return func(request, **args)


class Webhook(Endpoint):
    def post(self, request, signed_repo_slug):
        repo_slug = self.app.unsign(signed_repo_slug)
        project = self.app.get_project(repo_slug)
        project.trigger()
        logger.info('%s', project)
        return Response("")


def create_wsgi_app(app):
    url_map = Map([
        Rule('/hooks/<path:signed_repo_slug>', endpoint=Webhook(app)),
    ])

    def wsgi_app(environ, start_response):
        request = Request(environ)
        adapter = url_map.bind_to_environ(environ)
        logger.info("%s", request)
        print request
        try:
            endpoint, args = adapter.match()
            response = endpoint.dispatch(request, args)
        except HTTPException as e:
            response = e
        return response(environ, start_response)

    return wsgi_app
