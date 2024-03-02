from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    email = Column(String)
    date = Column(DateTime)
    daily_requests_count = Column(Integer)


class Brain(Base):
    __tablename__ = "brains"

    brain_id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship("BrainUser", back_populates="brain")
    vectors = relationship("BrainVector", back_populates="brain")


class BrainUser(Base):
    __tablename__ = "brains_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    brain_id = Column(Integer, ForeignKey("brains.brain_id"))
    rights = Column(String)

    user = relationship("User")
    brain = relationship("Brain", back_populates="users")


class BrainVector(Base):
    __tablename__ = "brains_vectors"

    vector_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    brain_id = Column(Integer, ForeignKey("brains.brain_id"))
    file_sha1 = Column(String)

    brain = relationship("Brain", back_populates="vectors")


class BrainSubscriptionInvitation(Base):
    __tablename__ = "brain_subscription_invitations"

    id = Column(Integer, primary_key=True)  # Assuming an integer primary key named 'id'
    brain_id = Column(String, ForeignKey("brains.brain_id"))
    email = Column(String, ForeignKey("users.email"))
    rights = Column(String)

    brain = relationship("Brain")
    user = relationship("User", foreign_keys=[email])


class ApiKey(Base):
    __tablename__ = "api_keys"

    key_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    api_key = Column(String, unique=True)
    creation_time = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    deleted_time = Column(DateTime, nullable=True)

    user = relationship("User")

class KnowledgeStream(Base):
    __tablename__ = "knowledge_stream"

    key_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    stream_name = Column(String, nullable=False)
    brain_ids = Column(String)
    stream_type = Column(String)  # pull / push
    stream_subtype = Column(String)  # http, kafka, database
    stream_parent = Column(String)
    stream_description = Column(String)
    stream_schedule = Column(String)
    knowledge_update_method = Column(String)  # merge / overwrite / mix
    knowledge_learning_prompt = Column(String)
    last_execute_date = Column(DateTime)
    deleted = Column(Boolean, default=False)

