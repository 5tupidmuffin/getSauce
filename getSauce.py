from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from log import logit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/getsauce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'SuperConfidentialKey'
app.permanent_session_lifetime = timedelta(days= 7)  # session lifespan

db = SQLAlchemy(app)

