from flask import Flask
from flask_bootstrap import Bootstrap
from container import Container
from src import APP_NAME


class StartUp(object):

    @staticmethod
    def build() -> Flask:
        app = Flask(APP_NAME)
        container = Container()
        app.env = container.environment
        app.container = container
        bootstrap = Bootstrap()
        bootstrap.init_app(app)

        return app
