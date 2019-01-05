def initialize_database(app, create_db=False, reset_db=False):
    from .flask_db import get_db
    db = get_db()
    db.init_app(app)

    from .models import Act, Person
    from .models import ActPerson

    if reset_db:
        app.logger.info("Resetting database")
        db.drop_all()
        db.session.commit()

    if create_db:
        app.logger.info("Creating database")
        db.create_all()
        db.session.commit()
