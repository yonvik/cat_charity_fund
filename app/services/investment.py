from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from datetime import datetime
from typing import Union, List

async def check_not_invested(
    session: AsyncSession,
):
    """Получение из БД первых по очереди незакрытых проектов и пожертвований."""
    project = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == 0
    ).order_by('create_date'))
    project = project.scalars().first()
    donation = await session.execute(select(Donation).where(
        Donation.fully_invested == 0
    ).order_by('create_date'))
    donation = donation.scalars().first()
    return project, donation


async def investment_process(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]]
) -> List[Union[CharityProject, Donation]]:
    target.invested_amount = target.invested_amount or 0
    count = 0
    for obj in sources:
        money = min(
            obj.full_amount - obj.invested_amount,
            target.full_amount - target.invested_amount
        )
        for item in [obj, target]:
            item.invested_amount += money
            if item.full_amount == item.invested_amount:
                item.close_date = datetime.now()
                item.fully_invested = True
        count += 1
        if target.fully_invested:
            break
    return sources[:count]
