import abc


class IRepertoireIOC:
    """
    Inversion of Control (i.e. Dependency Injection) interface for the Repertoire App
    """
    @classmethod
    @abc.abstractmethod
    def get_logger(cls):
        """
        Get the logger
        :return:
        """
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def get_dal(cls):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def get_db(cls):
        raise NotImplementedError()


class RepertoireIOC(IRepertoireIOC):

    _dal = None
    _db = None
    _logger = None

    @classmethod
    def get_logger(cls):
        if not cls._logger:
            from flask import current_app as app
            cls._logger = app.logger
        return cls._logger

    @classmethod
    def get_dal(cls):
        if not cls._dal:
            from repertoire.database.repertoire_dal import RepertoireDal
            cls._dal = RepertoireDal(db=cls.get_db(), logger=cls.get_logger())
        return cls._dal

    @classmethod
    def get_db(cls):
        if not cls._db:
            from repertoire.database.flask_db import get_db
            cls._db = get_db()
        return cls._db
