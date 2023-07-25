from flask import Flask
from startup import StartUp
from app.core.constants.app_metadata import APP_PORT
from core.utilities.startup import train_models

def main() -> None:
    app: Flask = StartUp().buid()

    app.run(port = APP_PORT)

    train_models(app.container.model_trainers)

if __name__ == "__main__":
    main()