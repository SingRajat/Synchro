from sqlalchemy import Column,String,Integer,Float,DateTime,JSON,ForeignKey,Text
from datetime import datetime
from app.db.connection import Base

class User(Base):
    __tablename__="users"

    id=Column(String, primary_key=True)
    name=Column(String, nullable=True)
    preferred_topics=Column(JSON, default=[])
    response_style=Column(String, default="detailed")
    created_at=Column(DateTime,default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__="chat_history"

    id=Column(Integer,primary_key=True, autoincrement=True)
    session_id=Column(String, index=True)
    user_id=Column(String)
    role=Column(String)
    content=Column(Text)
    timestamp=Column(DateTime,default=datetime.utcnow)

class Session_Summary(Base):
    __tablename__="session_summaries"

    session_id=Column(String,primary_key=True)
    Summary_text=Column(Text, default="")
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

class DocumentMetaData(Base):
    __tablename__="document_metadata"

    doc_id=Column(String, primary_key=True)
    user_id=Column(String)
    source_path=Column(String)
    created_at=Column(DateTime, default=datetime.utcnow)

class InteractionLog(Base):
    __tablename__="interaction_logs"

    id=Column(String, primary_key=True)
    session_id=Column(String)
    question=Column(Text)
    rewritten_query=Column(Text)
    retrieved_doc_ids=Column(JSON, default=[])

    answer=Column(Text)
    timestamp=Column(DateTime,default=datetime.utcnow)

class Feedback(Base):
    __tablename__="feedback"

    id=Column(Integer, primary_key=True, autoincrement=True)
    interaction_id=Column(String, ForeignKey("interaction_logs.id"))
    feedback=Column(Integer)
    timestamp=Column(DateTime, default=datetime.utcnow)

class DocumentScore(Base):
    __tablename__="document_scores"

    doc_id=Column(String, primary_key=True)
    feedback_score= Column(Float, default=0.0)
    usage_count=Column(Integer, default=0)