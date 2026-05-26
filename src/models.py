from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,Integer,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__ ='users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user") 
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user") 
    followers: Mapped[List["Follower"]] = relationship("Follower", back_populates="following_user") 
    follows: Mapped[List["Follower"]] = relationship("Follower", back_populates="follower_user") 


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username" : self.username,
            "firstname" : self.firstname,
            "lastname" : self.lastname,

            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    content: Mapped[str] = mapped_column(String(1000))
    user: Mapped["User"] = relationship("User", back_populates="posts") 
    medias: Mapped[List["Media"]] = relationship("Media", back_populates="post")

    def serialize(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "content" : self.content,
        }

class Media(db.Model):
    __tablename__= 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(String(1000))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'), nullable=False)
    post: Mapped["Post"] = relationship("Post", back_populates="medias")

    def serialize(self):
        return {
            "id" : self.id,
            "url" : self.url,
            "type" : self.type,
            "post_id" : self.post_id,
            
        }
    

class Comment(db.Model):
    __tablename__= 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="comments")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False) 
    


    def serialize(self):
        return {
            "id" : self.id,
            "text" : self.text,
            "user_id" : self.user_id,
            
        }
    
class Follower(db.Model):
    __tablename__= 'follower'
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    following_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    follower_user: Mapped["User"]= relationship("User", back_populates= "follower_user", foreign_keys=[follower_id])
    following_user: Mapped["User"]=relationship("User", back_populates= "following_user", foreign_keys=[following_id])