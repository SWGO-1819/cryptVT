from sqlalchemy.orm import Mapped, mapped_column

from config.database_config import database


class UserInfo(database.Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    ip: Mapped[str] = mapped_column(nullable=False)