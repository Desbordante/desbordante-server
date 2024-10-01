from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

type RelationalContextType = Session
type RelationalContextMakerType = sessionmaker

RelationalAddModel = DeclarativeBase
RelationalDeleteModel = DeclarativeBase
