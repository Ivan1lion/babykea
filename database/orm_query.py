from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserData, User
from database.engine import session_maker

from sqlalchemy import select


############# Добавление юзера в БД#############

async def orm_add_user(username: str | None = None):
    async with session_maker() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if not user:
            session.add(User(username=username))
            await session.commit()


############# Добавление запроса пользователя в БД#############

async def orm_user_request(session: AsyncSession, user_name: str, data: dict):
    obj = UserData(
        get_photo1=data['get_photo1'],
        get_photo2=data['get_photo2'],
        get_photo3=data['get_photo3'],
        get_comments=data['get_comments'],
        username=user_name
    )
    session.add(obj)
    await session.commit()