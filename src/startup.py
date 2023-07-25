from flask import Flask
from flask_bootstrap import Bootstrap
from container import Container
from core.constants.app_metadata import APP_NAME

class StartUp(object):

    def __init__(self) -> None:
        pass

    def buid(self) -> Flask:
        app = Flask(APP_NAME)
        container = Container()
        app.env = container.environment
        app.container = container
        bootstrap = Bootstrap()
        bootstrap.init_app(app)

        return app        