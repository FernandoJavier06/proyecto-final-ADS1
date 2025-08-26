# app/models.py
from .extensions import db
from datetime import datetime
import enum
from flask_login import UserMixin

# Imports adicionales para el estilo moderno de SQLAlchemy 2.0
from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

# --- Enum para los roles ---
# Usamos la herencia de 'str' que es una práctica robusta
class RoleEnum(str, enum.Enum):
    admin = 'administrador'
    manager = 'gerente'
    cashier = 'cajero'
    warehouseWorker = 'bodeguero'

# --- Modelo Person con sintaxis moderna ---
class Person(db.Model):
    __tablename__ = 'Person'

    # Mapeo explícito con type hints y mapped_column
    personId: Mapped[int] = mapped_column('personId', Integer, primary_key=True)
    name: Mapped[str] = mapped_column('name', String(55), nullable=False)
    middleName: Mapped[str | None] = mapped_column('middleName', String(55), nullable=True)
    surname: Mapped[str] = mapped_column('surname', String(55), nullable=False)

    # Relación bidireccional con User
    user: Mapped["User"] = relationship(back_populates="person")

    def __repr__(self):
        return f'<Person {self.name} {self.surname}>'

# --- Modelo User con sintaxis moderna ---
class User(db.Model, UserMixin):
    __tablename__ = 'User'
    
    def get_id(self):
        return self.userId

    userId: Mapped[int] = mapped_column('userId', Integer, primary_key=True)
    userEmail: Mapped[str] = mapped_column('userEmail', String(45), unique=True, nullable=False)
    password: Mapped[str] = mapped_column('password', String(128), nullable=False)
    
    # --- La solución definitiva para el Enum ---
    # Le decimos explícitamente a SQLAlchemy qué valores de string esperar
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
    
    # Definición de la llave foránea
    personId: Mapped[int] = mapped_column('personId', ForeignKey('Person.personId'), nullable=False, unique=True)

    # Relación bidireccional con Person
    person: Mapped["Person"] = relationship(back_populates="user")

    # --- Métodos para manejo seguro de contraseñas (sin cambios) ---
    def set_password(self, password_to_set):
        from .extensions import bcrypt
        self.password = bcrypt.generate_password_hash(password_to_set).decode('utf-8')

    def check_password(self, password_to_check):
        from .extensions import bcrypt
        return bcrypt.check_password_hash(self.password, password_to_check)

    def __repr__(self):
        return f'<User {self.userEmail}>'

