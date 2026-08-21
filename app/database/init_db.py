from app.database.database import Base, engine
def init_database():

    print("Creating EduAccess AI database...")

    Base.metadata.create_all(
        bind=engine
    )

    print("Database created successfully.")


if __name__ == "__main__":

    init_database()