from flask import Flask

from app import create_app, db
from tests.utils import populate_posts, populate_users


def before_scenario(context, feature):
    app: Flask = create_app(environment="testing")
    app.config["TESTING"] = True
    
    context.app_ctx = app.app_context()
    context.app_ctx.push()
    db.drop_all()
    db.create_all()
    context.client = app.test_client()
    populate_users()
    populate_posts()


def after_scenario(context, feature):
    db.session.remove()
    db.drop_all()
    context.app_ctx.pop()
