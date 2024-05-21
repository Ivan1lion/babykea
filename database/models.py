from sqlalchemy import String, Text, DateTime, func, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(150))
    # payment: Mapped[str] = mapped_column(Text)

class UserData(Base):
    __tablename__ = "userdatas"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    get_photo1: Mapped[str] = mapped_column(String(150))
    get_photo2: Mapped[str] = mapped_column(String(150))
    get_photo3: Mapped[str] = mapped_column(String(150))
    get_comments: Mapped[str] = mapped_column(Text)
    username: Mapped[str] = mapped_column(String(150))