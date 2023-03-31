from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

from db.engine import engine


class BaseModel(DeclarativeBase):
    pass


class Device(BaseModel):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    manufacturer: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    versions: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<Device name={self.name}>"


class Fingerprint(BaseModel):
    __tablename__ = "prints"

    id: Mapped[int] = mapped_column(primary_key=True)
    print: Mapped[str] = mapped_column(nullable=False)
    build_description: Mapped[str] = mapped_column(nullable=False)
    product_brand: Mapped[str] = mapped_column(nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    product_device: Mapped[str] = mapped_column(nullable=False)
    product_version: Mapped[str] = mapped_column(nullable=False)
    build_id: Mapped[str] = mapped_column(nullable=False)
    build_type: Mapped[str] = mapped_column(nullable=False)
    build_tags: Mapped[str] = mapped_column(nullable=False)
    incremental: Mapped[str] = mapped_column(nullable=False)
    security_patch: Mapped[str] = mapped_column(nullable=True)

    brand_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Fingerprint name={self.print}>"


# BaseModel.metadata.create_all(engine)
