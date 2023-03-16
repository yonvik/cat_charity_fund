from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession


def investment_process(session: AsyncSession, obj):
    """Инвестирование пожертвований в незакрытые проекты."""
    session.invested_amount = session.invested_amount or 0
    count = 0
    for balance in obj:
        donation = min(
            balance.full_amount - balance.invested_amount,
            session.full_amount - session.invested_amount
        )
        for project in [balance, session]:
            project.invested_amount += donation
            if project.full_amount == project.invested_amount:
                project.close_date = datetime.now()
                project.fully_invested = True
        count += 1
        if session.fully_invested:
            break
    return obj[:count]
