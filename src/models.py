import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Tabla de Usuarios
class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    following = relationship('Follower', 
                             foreign_keys='Follower.user_from_id',
                             backref=backref('follower', lazy='joined'))
    followers = relationship('Follower', 
                             foreign_keys='Follower.user_to_id',
                             backref=backref('followed', lazy='joined'))

# Tabla de Post
class Post(Base):
    __tablename__ = 'Post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)

    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

# Tabla de Comentarios
class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

# Tabla de Media
class Media(Base):
    __tablename__ = 'Media'

    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video'), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)

    post = relationship('Post', back_populates='media')

# Tabla de Seguidores (Follower)
class Follower(Base):
    __tablename__ = 'Follower'

    user_from_id = Column(Integer, ForeignKey('User.id'), primary_key=True)  # Usuario que sigue
    user_to_id = Column(Integer, ForeignKey('User.id'), primary_key=True)  # Usuario seguido

# Crear el diagrama
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
