from unittest.mock import Mock


# See https://stackoverflow.com/a/16976500/1299271
class AnyStringWith(str):
    """
    Matches with Mock function string arguments that contain a provided
    substring.
    """
    def __eq__(self, other):
        return self in other


# See https://stackoverflow.com/a/54838760/1299271
def assert_not_called_with(self, *args, **kwargs):
    """
    Asserts that a Mock function was never called with specified arguments.
    """
    try:
        self.assert_called_with(*args, **kwargs)
    except AssertionError:
        return
    raise AssertionError('Expected %s to not have been called.' % self._format_mock_call_signature(args, kwargs))


Mock.assert_not_called_with = assert_not_called_with
