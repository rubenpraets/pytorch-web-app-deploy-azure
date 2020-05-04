"""Initialize app."""
from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES

photos = UploadSet('photos', IMAGES)

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        from . import routes
        configure_uploads(app, photos)
        return app
