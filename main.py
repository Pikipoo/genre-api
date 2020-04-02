from genre_api.models.meta import sqlite_db as database
from genre_api.api import create_app, create_api, create_routes, create_tables

app = create_app()
api = create_api(app)
create_tables()
create_routes(api)


@app.before_request
def before_request():
    database.connect()


@app.after_request
def after_request(response):
    database.close()
    return response


if __name__ == '__main__':
    app.run(debug=True)
