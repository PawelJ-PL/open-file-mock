from unittest.mock import MagicMock
import io


DEFAULTS_EXCEPTION = 'exception'
DEFAULTS_MOCK = 'mock'
DEFAULTS_ORIGINAL = 'original'


class MockOpen:
    def __init__(self, when_not_registered=DEFAULTS_EXCEPTION):
        self.default_behavior = when_not_registered
        self._path_mappings = {}

    def register_object_for_path(self, path, obj):
        if path in self._path_mappings.keys():
            raise ValueError('Path {0} already registered with object {1}'.format(path, self._path_mappings[path]))
        self.update_object_for_path(path, obj)

    def update_object_for_path(self, path, obj):
        self._path_mappings[path] = obj

    def unregister_path(self, path):
        del self._path_mappings[path]

    def set_read_data_for(self, path, data):
        mock = MagicMock()
        mock.read.return_value = data
        mock.__enter__.return_value = mock
        self.register_object_for_path(path, mock)

    def get_object_for_path(self, path):
        return self._path_mappings[path]

    def __call__(self, *args, **kwargs):
        path = kwargs.get('file') or args[0]
        try:
            return self._path_mappings[path]
        except KeyError:
            if self.default_behavior == DEFAULTS_EXCEPTION:
                raise FileNotFoundError('File {} not found in mock function'.format(path))
            elif self.default_behavior == DEFAULTS_ORIGINAL:
                return self._get_orig_file(*args, **kwargs)
            elif self.default_behavior == DEFAULTS_MOCK:
                mock = MagicMock()
                self._path_mappings[path] = mock
                return mock
            else:
                raise ValueError('{} is not valid default behavior'.format(self.default_behavior))

    @staticmethod
    def _get_orig_file(*args, **kwargs):
        if not isinstance(open, MockOpen) and isinstance(io.open, MockOpen):
            return open(*args, **kwargs)
        elif isinstance(open, MockOpen) and isinstance(io.open, MockOpen):
            raise RuntimeError('Both open and io.open already patched')
        else:
            return io.open(*args, **kwargs)
