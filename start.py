from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import os
basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_URL').replace("postgres://", "postgresql://") or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
db.init_app(app)

class PageGets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)

@app.route('/')
def home():   
    listen = PageGets(date = datetime.utcnow())
    db.session.add(listen)
    db.session.commit()
    return render_template('index.html', count=PageGets.query.count())


with app.app_context():
    print("creating tables...")
    db.create_all()
    print("created!")