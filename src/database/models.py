from sqlalchemy import Column, String, Boolean, Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime

Base = declarative_base()


photo_m2m_tag = Table(
    "photo_m2m_tag",
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('photo', Integer, ForeignKey('photos.id', ondelete='CASCADE')),
    Column('tag', Integer, ForeignKey('tags.id', ondelete='CASCADE'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    token = Column(String(150))
    role = Column(String(20), nullable=False)
    is_verify = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime)

    photos = relationship('Photo', cascade='all, delete', backref='users')
    comments = relationship('Comment', cascade='all, delete', backref='users')
    rates = relationship('Rate', cascade='all, delete', backref='users')


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    description = Column(String(255))
    modify_url = Column(String(255))
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))

    tags = relationship('Tag', secondary=photo_m2m_tag, backref='photos', passive_deletes=True)
    comments = relationship('Comment', cascade='all, delete', backref='photos')
    rates = relationship('Rate', cascade='all, delete', backref='photos')


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(20), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime)


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    photo_id = Column(Integer, ForeignKey(Photo.id, ondelete='CASCADE'))


class Rate(Base):
    __tablename__ = 'rates'
    id = Column(Integer, primary_key=True)
    rate = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    photo_id = Column(Integer, ForeignKey(Photo.id, ondelete='CASCADE'))


