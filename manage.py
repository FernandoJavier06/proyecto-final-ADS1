# manage.py
from app import create_app
from app.extensions import db
from app.models import User, Person, RoleEnum
import click

# Crea una instancia de la app para poder usar su contexto
app = create_app()

@app.cli.command("create-user")
@click.argument("name")
@click.argument("surname")
@click.argument("email")
@click.argument("password")
@click.option("--role", default="admin", help="Rol del usuario (admin, manager, cashier, warehouseWorker)")
def create_user(name, surname, email, password, role):
    """Crea un nuevo usuario en la base de datos con la contraseña hasheada."""
    with app.app_context():
        # Verifica si el usuario ya existe
        if User.query.filter_by(userEmail=email).first():
            print(f"Error: El usuario con email '{email}' ya existe.")
            return

        # Crea la persona asociada
        new_person = Person(name=name, surname=surname)
        db.session.add(new_person)
        db.session.flush() # Para obtener el personId antes de hacer commit

        # Crea el usuario
        new_user = User(
            userEmail=email,
            personId=new_person.personId,
            role=RoleEnum(role) # Convierte el string del rol al miembro del Enum
        )
        
        # ¡Usa el método para hashear la contraseña!
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        print(f"¡Usuario '{email}' creado exitosamente con el rol de '{role}'!")