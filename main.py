import configparser
import logging
import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text, exc

dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(f'{dir_path}/config.cfg')

logging.basicConfig(filename=f"{dir_path}/{config['LOG']['log_file']}", level=config['LOG']['log_level'])

app = Flask(__name__)
connection_string = 'mysql://' + config['DATABASE']['mysql_user'] + ':' + \
                    config['DATABASE']['mysql_password'] + '@' + \
                    config['DATABASE']['msql_host'] + '/' + \
                    config['DATABASE']['mysql_database']

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
db = SQLAlchemy(app)


# create table user (   id INT NOT NULL AUTO_INCREMENT,
#                       name VARCHAR(100),
#                       surname VARCHAR(100),
#                       email VARCHAR(100),
#                       PRIMARY KEY (id));

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.VARCHAR(50))
    surname = db.Column(db.VARCHAR(50))
    email = db.Column(db.VARCHAR(50))

    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email

    def json(self):
        data = {'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'email': self.email}

        return data


def parse():
    data = {'id': request.args.get('id'),
            'name': request.args.get('name'),
            'surname': request.args.get('surname'),
            'email': request.args.get('email')}

    return data


@app.route('/', methods=['GET'])
def select_get():
    data = parse()

    if data['id'] is None:
        query = User.query.order_by(User.id).all()

        if len(query) == 0:
            return "Couldn't find any user", 200

        return jsonify(users=[i.json() for i in query]), 200

    else:
        query = User.query.filter_by(id=data['id']).first()

        if query is None:
            return "Couldn't find user with this id", 200

        return jsonify(query.json()), 200


@app.route('/', methods=['POST', 'PUT'])
def insert_post_put():
    data = parse()

    user = User(data['name'], data['surname'], data['email'])
    db.session.add(user)
    db.session.commit()

    return "Success", 200


@app.route('/', methods=['DELETE'])
def delete_delete():
    data = parse()
    user = User.query.filter_by(id=data['id']).first()

    if user is None:
        return "Could not find user with this ID", 200

    db.session.delete(user)
    db.session.commit()

    return "Success", 200


def main():
    # Connectivity test
    try:
        engine = create_engine(connection_string)
        engine.connect().execute(text("SHOW TABLES;"))
    except exc.OperationalError as e:
        logging.error("Incorrect login credentials")
        logging.error(str(e))

        exit(1)

    # Test table
    try:
        engine.connect().execute(text("SELECT * FROM user;"))
    except exc.ProgrammingError as e:
        logging.error("Table 'denis_kaynar_python.user' doesn't exist")
        logging.error(e)

        exit(1)

    app.run(host=config['API']['host'], port=config['API']['port'])


if __name__ == "__main__":
    main()
