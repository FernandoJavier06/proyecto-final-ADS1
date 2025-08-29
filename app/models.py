# app/models.py
from .extensions import db
from datetime import datetime
import enum
from flask_login import UserMixin
from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, Enum as SQLAlchemyEnum, DECIMAL, SMALLINT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

class RoleEnum(str, enum.Enum):
    admin = 'administrador'
    manager = 'gerente'
    cashier = 'cajero'
    warehouseWorker = 'bodeguero'

class OriginTypeEnum(str, enum.Enum):
    sale = 'venta'
    purchase = 'compra'
    saleReturn = 'dev venta'
    purchaseReturn = 'dev compra'
    
class Person(db.Model):
    __tablename__ = 'Person'
    personId: Mapped[int] = mapped_column('personId', Integer, primary_key=True)
    name: Mapped[str] = mapped_column('name', String(55), nullable=False)
    middleName: Mapped[str | None] = mapped_column('middleName', String(55), nullable=True)
    surname: Mapped[str] = mapped_column('surname', String(55), nullable=False)
    user: Mapped["User"] = relationship(back_populates="person")
    def __repr__(self):
        return f'<Person {self.name} {self.surname}>'

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    def get_id(self):
        return self.userId
    userId: Mapped[int] = mapped_column('userId', Integer, primary_key=True)
    userEmail: Mapped[str] = mapped_column('userEmail', String(45), unique=True, nullable=False)
    password: Mapped[str] = mapped_column('password', String(128), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        'role', 
        SQLAlchemyEnum(
            RoleEnum, 
            native_enum=False,
            values_callable=lambda x: [e.value for e in x]
        ), 
        nullable=False, 
        default=RoleEnum.cashier
    )
    createdAt: Mapped[datetime] = mapped_column('createdAt', TIMESTAMP, default=datetime.utcnow)
    personId: Mapped[int] = mapped_column('personId', ForeignKey('Person.personId'), nullable=False, unique=True)
    person: Mapped["Person"] = relationship(back_populates="user")
    def set_password(self, password_to_set):
        from .extensions import bcrypt
        self.password = bcrypt.generate_password_hash(password_to_set).decode('utf-8')
    def check_password(self, password_to_check):
        from .extensions import bcrypt
        return bcrypt.check_password_hash(self.password, password_to_check)
    def __repr__(self):
        return f'<User {self.userEmail}>'

class Brand(db.Model):
    __tablename__ = 'Brand'
    brandId: Mapped[int] = mapped_column(SMALLINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

class Product(db.model):
    __tablename__ = 'Product'
    productId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brandId: Mapped[int] = mapped_column(ForeignKey('Brand.brandId'))
    name: Mapped[str] = mapped_column(String(100), nullable=False)

class Presentation(db.Model):
    __tablename__ = 'Presentation'
    presentationId: Mapped[int] = mapped_column(SMALLINT, primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
class UnitMeasure(db.Model):
    __tablename__ = 'UnitMeasure'
    unitMeasureId: Mapped[int] = mapped_column(TINYINT,primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(50),nullable=False)

class ProductVariant(db.Model):
    __tablename__ = 'ProductVariant'
    productVariantId: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    productId: Mapped[int] = mapped_column(ForeignKey('Product.productId'))
    presentationId: Mapped[int] = mapped_column(ForeignKey('Presentation.presentationId'))
    unitMeasureId: Mapped[int] = mapped_column(ForeignKey('UnitMeasure.unitMeasureId'))
    size: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    product: Mapped["Product"] = relationship()
    
class Warehouse(db.Model):
    __tablename__ = 'Warehouse'
    warehouseId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    location: Mapped[str | None] = mapped_column(String(45))

class InventoryStock(db.Model):
    __tablename__ = 'InventoryStock'
    productVariantId: Mapped[int] = mapped_column(ForeignKey('ProductVariant.productVariantId'), primary_key=True)
    warehouseId: Mapped[int] = mapped_column(ForeignKey('Warehouse.warehouseId'), primary_key=True)
    quantityOnHand: Mapped[int] = mapped_column(Integer, default=0)
    averageCost: Mapped[float] = mapped_column(DECIMAL(10,2), default=0.00)

class Sale(db.Model):
    __tablename__ = 'Sale'
    saleId: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP,default=datetime.utcnow)
    details: Mapped[list["SaleDetail"]] = relationship()

class SaleDetail(db.Model):
    __tablename__ = 'SaleDetail'
    saleId: Mapped[int] = mapped_column(ForeignKey('Sale.saleId'), primary_key=True)
    productVariantId: Mapped[int] = mapped_column(ForeignKey('ProductVariant.productVariantId'),primary_key=True)
    quantity: Mapped[int] = mapped_column(SMALLINT, nullable=False)
    subtotal: Mapped[float] = mapped_column(DECIMAL(10,2),nullable=False)
    unitPrice: Mapped[float] = mapped_column(DECIMAL(10,2),nullable=False)

class Movement(db.Model):
    __tablename__ = 'Movement'
    movementId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    productVariantId: Mapped[int] = mapped_column(ForeignKey('ProductVariant.productVariantId'))
    warehouseId: Mapped[int] = mapped_column(ForeignKey('Warehouse.warehouseId'))
    originId: Mapped[int | None] = mapped_column(Integer)
    originType: Mapped[OriginTypeEnum | None] = mapped_column(SQLAlchemyEnum(
        OriginTypeEnum, 
        native_enum=False, 
        values_callable=lambda x: [e.value for e in x]))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unitCost: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    balanceQuantity: Mapped[int] = mapped_column(Integer, nullable=False)
    balanceUnitCost: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    balanceTotalCost: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    product_variant: Mapped["ProductVariant"] = relationship()
    warehouse: Mapped["Warehouse"] = relationship()