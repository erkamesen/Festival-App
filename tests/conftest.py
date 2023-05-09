import pytest

from apps import create_app, db



class TestConfig(object):
    
    # Set up the App SECRET_KEY
    SECRET_KEY  = "thisisasecretkey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USE_SQLITE  = True 
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    

@pytest.fixture()
def app():
    app = create_app(config=TestConfig)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://" # in memory

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
    