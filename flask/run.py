from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from puweb.new.app.services.dbmanage.db_manager import DatabaseManager
from datetime import datetime
from flask_migrate import Migrate

from app.__init__ import db,create_app

app = create_app()
migrate = Migrate(app, db)

def init_test_data():
    pass

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':

    # init_test_data()
    app.run(debug=True)
