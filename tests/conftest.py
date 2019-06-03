import pytest
from app import create_app
from mongoengine import connect
from db_seed import mongo_db_seed


@pytest.fixture(scope="module")
def app():
    test_db_name = "bookstore_db_test_1"
    db_conn = connect(test_db_name, host='localhost', port=27017)

    app = create_app({
        'TESTING': True,
        'MONGODB_SETTINGS': {
            'db': test_db_name,
            'host': 'localhost',
            'port': 27017
        }
    })

    with app.app_context():
        mongo_db_seed(test_db_name)

    yield app

    db_conn.drop_database(test_db_name)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
