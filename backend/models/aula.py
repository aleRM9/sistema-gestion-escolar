from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Aula(Base): 
    __tablename__ = "aulas"

    aula_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo:Mapped[str] = mapped_column(String(10), nullable=False)
    ubicacion: Mapped[str] = mapped_column(String(100), nullable=False)
    