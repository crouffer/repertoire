import pytest


class TestExamples(object):
    @staticmethod
    def test_true():
        assert True

    @staticmethod
    def test_false():
        assert (not True) is False

    @staticmethod
    def test_string_contains():
        x = 'this'
        assert 'h' in x

    @staticmethod
    def test_key_in_dict():
        x = {
            "my_attr": "attr_value"
        }
        assert 'my_attr' in x

    @staticmethod
    @pytest.mark.xfail
    def test_expected_failure():
        assert False

    @staticmethod
    @pytest.mark.skip
    def test_skipped_test():
        assert False

    SKIP_THIS_TEST = True

    @staticmethod
    @pytest.mark.skipif(SKIP_THIS_TEST, reason="SKIP_THIS_TEST is set to True")
    def test_conditional_skip():
        assert True
