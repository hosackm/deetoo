from sqlalchemy import create_engine
from .base import Base
from pathlib import Path


HERE = Path(__file__).parents[3]
DB_FILEPATH = f"sqlite:///{str(HERE)}/example.db"


engine = create_engine(DB_FILEPATH)
Base.metadata.create_all(engine)
