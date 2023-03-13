from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD:

    def __init__(self, model) -> None:
        self.model = model

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[int] = None
    ):
        """Создание объекта и сохранение в БД."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ):
        """Получение объекта из БД по id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        """Получение всех обьектов из БД."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()
