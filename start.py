from datetime import datetime
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os
basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_URL', '').replace("postgres://", "postgresql://") or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class PageGets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)

@app.route('/')
def home():   
    count = 0
    try:
        listen = PageGets(date = datetime.utcnow())
        db.session.add(listen)
        db.session.commit()
        count=PageGets.query.count()
    except:
        count="ERROR"
        pass
    return render_template('index.html', count=count)
