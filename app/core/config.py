from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot.'
    app_description: str = 'Фонд сбора средств, направленные на помощь котиков.'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = 'secret'
    superuser_email: Optional[EmailStr] = None
    superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
