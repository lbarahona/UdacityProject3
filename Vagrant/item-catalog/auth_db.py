''' This module holds most of the items related to github oauth login
 and the related sqlite user database '''

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


authBase = declarative_base()


class User(authBase):
    """ this class is used when dealing with Oauth user data stored
     in an sqlite database for sqlalchemy and github-flask"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    github_access_token = Column(String(200))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

auth_engine = create_engine('sqlite:///auth.db')

db_session = scoped_session(sessionmaker(auth_engine))

authBase.query = db_session.query_property()


def get_user_by_id(id_num):
    """ returns the Oauth user associated with this id """
    target_user = db_session.query(User).filter_by(id=id_num).one()
    return target_user


def add_user_name(id_num, user_name):
    """ adds a user to the Oauth user database """
    target_user = get_user_by_id(id_num)
    if target_user != []:
        target_user.username = user_name
        db_session.commit()


def empty_users():
    """ removes all Oauth users.  This should have additional checks added
    before using it in the production environment """
    db_session.query(User).delete()
    db_session.commit()

authBase.metadata.create_all(bind=auth_engine)
