import pytest
from repertoire.common.repertoire_ioc import IRepertoireIOC, RepertoireIOC


def test_constructor():
    uut = RepertoireIOC()
    assert isinstance(uut, IRepertoireIOC)


def test_get_logger():
    uut = RepertoireIOC()
    logger = uut.get_logger()
    assert logger is not None


def test_get_logger_interface_not_implemented():
    class MyIoc(IRepertoireIOC):
        def __init__(self):
            pass

    uut = MyIoc()
    assert uut is not None

    with pytest.raises(NotImplementedError):
        uut.get_logger()
