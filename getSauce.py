from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLITE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'SuperConfidentialKey'
app.permanent_session_lifetime = timedelta(days= 7)  # session lifespan

db = SQLAlchemy(app)

