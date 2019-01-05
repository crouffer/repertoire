from repertoire.database.i_repertoire_dal import IRepertoireDal


class RepertoireDal(IRepertoireDal):

    @classmethod
    def __init__(cls, db=None, logger=None):
        if not db:
            from repertoire.common.repertoire_ioc import RepertoireIOC as ri
            cls.db = ri.get_db()
        else:
            cls.db = db

        if not logger:
            cls.logger = ri.get_logger()
        else:
            cls.logger = logger

    @classmethod
    def add_person(cls, first_name, last_name):
        from .models import Person
        p = Person()
        p.first_name = first_name
        p.last_name = last_name
        cls.db.session.add(p)
        cls.db.session.commit()

        return p

    @classmethod
    def delete_person(cls, person_id):
        from .models import Person
        p = cls.db.session.query(Person) \
            .filter(Person.id == person_id).one()
        cls.db.session.delete(p)
        cls.db.session.commit()

    @classmethod
    def get_person(cls, first_name, last_name):
        from .models import Person
        query = cls.db.session.query(Person) \
            .filter(Person.first_name == first_name,
                    Person.last_name == last_name)

        return query.all()

    @classmethod
    def get_person_list(cls, offset=None, limit=None):
        from .models import Person
        query = cls.db.session.query(Person)

        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        return query.all()
