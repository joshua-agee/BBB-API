from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.postgres_ext import *

db = PostgresqlExtDatabase('postgres', user='postgres', password='123456')
class BaseModel(Model):
    class Meta:
        database = db #use a root class to specify database for all models

class User(BaseModel, UserMixin):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()

class Recipe(BaseModel):
    name = CharField()
    summary = TextField()
    ingredients = BinaryJSONField()
    directions = BinaryJSONField()
    source = CharField()
    contributor = ForeignKeyField(User, backref='recipes')
    likes = IntegerField()
    photo = CharField()

class Comment(BaseModel):
    by_user = ForeignKeyField(User, backref='comments')
    on_recipe = ForeignKeyField(Recipe, backref='comments')
    title = CharField()
    comment = TextField()
    photo = CharField()

class Like(BaseModel):
    by_user = ForeignKeyField(User, backref='likes')
    on_recipe = ForeignKeyField(Recipe, backref='likes')

def initialize():
    db.connect()
    db.create_tables([User, Recipe, Comment, Like], safe=True)
    print('tables created')
    db.close()