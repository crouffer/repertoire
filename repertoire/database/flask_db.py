from flask_sqlalchemy import SQLAlchemy


def get_db() -> SQLAlchemy:
    try:
        from flask import g
        g_db = getattr(g, '_database', None)
        if g_db is None:
            new_db = SQLAlchemy()
            g._database = new_db
            return new_db
        else:
            return g_db
    except Exception:
        raise

