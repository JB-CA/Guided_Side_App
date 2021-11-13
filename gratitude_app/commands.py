from main import db
from flask import Blueprint

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    """Creates the database."""
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    """Drops the database."""
    db.drop_all()
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    """Seeds the database."""
    from models.users import User
    from models.gratitudes import Gratitude
    from faker import Faker
    fake = Faker()

    for i in range(5):
        user = User(
            name = fake.name(),
            email = fake.email(),
            password= fake.password()
        )
        db.session.add(user)

    db.session.commit()

    # Get users from database
    users = User.query.all()

    for user in users:
        # get random number of gratitudes
        num_gratitudes = fake.random_int(min=1, max=3)
        for i in range(num_gratitudes):
            gratitude = Gratitude(
                user_id = user.user_id,
                name = fake.name(),
                text = fake.sentence(),
                image = fake.url()
            )
            db.session.add(gratitude)

    print("Seeded the database")

@db_commands.cli.command("reset")
def reset_db():
    """Resets the database."""
    db.drop_all()
    db.create_all()    
    from models.users import User
    from models.gratitudes import Gratitude
    from faker import Faker
    fake = Faker()

    for i in range(5):
        user = User(
            name = fake.name(),
            email = fake.email(),
            password= fake.password()
        )
        db.session.add(user)

    db.session.commit()

    # Get users from database
    users = User.query.all()

    for user in users:
        # get random number of gratitudes
        num_gratitudes = fake.random_int(min=1, max=3)
        for i in range(num_gratitudes):
            gratitude = Gratitude(
                name = fake.name(),
                user_id = user.user_id,
                text = fake.sentence(),
                image = fake.url()
            )
            db.session.add(gratitude)

    db.session.commit()

    print("Database Reset")