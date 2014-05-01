from sqlalchemy.ext.declaritive import delcarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, Table, String, ForeignKey

Base = delcarative_base()


class User(Base):
    __tablename__ = 'users'
    username = Column(String(100), primary_key=True)
    lastUpdated = Column(Integer)
    postCount = Column(Integer)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), ForeignKey('users.username'))
    type = Column(String(20))
    date = Column(Integer)
    noteCount = Column(Integer)

    author = relationship("User", backref=backref('posts', order_by=id))


tag_to_post = Table('association', Base.metadata,
                    Column('postId', Integer, ForeignKey('posts.id')),
                    Column('body', String(100), ForeignKey('tags.body'))
                    )


class Tag(Base):
    __tablename__ = 'tags'
    body = Column(String(100), primary_key=True)


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), ForeignKey('users.username'))
    rebloggedFrom = Column(String(100))
    postId = Column(Integer, ForeignKey('posts.id'))
    type = Column(String(20))

    user = relationship("User", backref=backref('notes', order_by=id))
    post = relationship("Post", backref=backref('notes', order_by=id))
