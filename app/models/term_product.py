from sqlalchemy import PrimaryKeyConstraint
from sqlmodel import Field, SQLModel


class TermProduct(SQLModel, table=True):
    sku: str = Field(foreign_key="product.sku")
    term_code: str = Field(foreign_key="term.term_code")

    __tablename__ = "term_product"
    __table_args__ = (PrimaryKeyConstraint("sku", "term_code"),)