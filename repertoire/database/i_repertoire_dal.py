class IRepertoireDal:
    @classmethod
    def add_person(cls, first_name, last_name):
        raise NotImplementedError()

    @classmethod
    def delete_person(cls, person_id):
        raise NotImplementedError()

    @classmethod
    def get_person(cls, first_name, last_name):
        raise NotImplementedError()

    @classmethod
    def get_person_list(cls, offset, limit):
        raise NotImplementedError()
