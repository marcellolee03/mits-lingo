from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str]
    answers: Mapped[list[str]] = mapped_column(JSON)
