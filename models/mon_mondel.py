from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os


"""
Ces classes et leurs relations forment la structure de la base de données
de votre application et permettent de stocker des informations sur les utilisateurs,
 les sessions, les pays et les langues.

"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_HOST = "localhost"
DATABASE_NAME = "database_nlc"
DATABASE_USERNAME = "root"
DATABASE_PASSWORD = "root"

engine = create_engine(f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}")

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

user_country_association = Table('user_country_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('country_id', Integer, ForeignKey('countries.id'))
)

user_language_association = Table('user_language_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('language_id', Integer, ForeignKey('languages.id'))
)

class User(Base):
    """
    Elle contient les informations des utilisateurs de l'application. 
    Les utilisateurs sont caractérisés par un identifiant unique (id),
    un nom d'utilisateur (username) et un mot de passe (password)
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    countries = relationship('Country', secondary=user_country_association, back_populates='users')
    languages = relationship('Language', secondary=user_language_association, back_populates='users')
    sessions = relationship('Session', back_populates='user')

class Session(Base):
    """
    Elle stocke des informations sur les sessions d'utilisation de l'application.
    Chaque session est associée à un utilisateur, 
    identifié par son user_id. Les autres champs incluent le texte de la conversation généré (generated_code), 
    le texte du prompt (prompt), et la date de création (created_at)
    """
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    prompt = Column(String(2550), nullable=False)
    generated_code = Column(String(2550), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='sessions')

class Country(Base):
    """
    Elle est utilisée pour stocker des informations sur les pays. 
    Chaque pays a un nom unique (name). 
    La classe Country est associée à la classe User via une relation many-to-many, 
    ce qui signifie qu'un utilisateur peut être associé à plusieurs pays
    """
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    users = relationship('User', secondary=user_country_association, back_populates='countries')
    def __init__(self, name):
        self.name = name

class Language(Base):
    """
    Elle est utilisée pour stocker des informations sur les langues. 
    Chaque langue a un nom unique (name). 
    Comme la classe Country, la classe Language est associée à la classe User via une relation many-to-many, 
    permettant à un utilisateur d'être associé à plusieurs langues.
    """
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    users = relationship('User', secondary=user_language_association, back_populates='languages')
    def __init__(self, name):
        self.name = name

Base.metadata.create_all(engine)


Base.metadata.create_all(engine)

session.close()
