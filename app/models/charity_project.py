from sqlalchemy import Column, String, Text

from app.models.abstractclass import BaseClass


class CharityProject(BaseClass):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'name: {self.name[:16]}, '
            f'description: {self.description[:16]}, '
            f'{super().__repr__()}'
        )
