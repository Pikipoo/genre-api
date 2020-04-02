import pytest
from genre_api.api import create_app, create_api, create_routes, create_tables


@pytest.fixture(scope='class')
def app_class(request):
    """
    The app_class fixture declares a Flask test_client, called in every
    API related unit tests.
    """
    app = create_app()

    app.config['TESTING'] = True
    # Default port is 5000
    app.config['LIVESERVER_PORT'] = 8943
    # Default timeout is 5 seconds
    app.config['LIVESERVER_TIMEOUT'] = 10

    api = create_api(app)
    create_routes(api)

    request.cls.app = app
    request.cls.client = app.test_client()
