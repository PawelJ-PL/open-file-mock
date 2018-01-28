from os import unlink
from os.path import join, dirname
from tempfile import mkstemp
import io
from unittest import TestCase
from unittest.mock import patch, MagicMock
from open_file_mock import MockOpen, DEFAULTS_MOCK, DEFAULTS_ORIGINAL, DEFAULTS_EXCEPTION
import open_file_mock.tests as test_module


class TestOpenFileMock(TestCase):

    class CustomObj:
        def read(self):
            return 'read'

        def write(self):
            return 'write'

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return 'exit'

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_raise_exception_when_file_not_found_and_default_settings_without_context_manager(self, open_mock):
        with self.assertRaisesRegex(FileNotFoundError, 'File /path/to/file not found in mock function'):
            open('/path/to/file')

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_raise_exception_when_file_not_found_and_default_settings_with_context_manger(self, open_mock):
        with self.assertRaisesRegex(FileNotFoundError, 'File /path/to/file not found in mock function'):
            with open('/path/to/file'):
                pass

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_return_new_mock_when_defaults_exception_and_file_not_registered(self, open_mock):
        # given
        open_mock.default_behavior = DEFAULTS_EXCEPTION

        # when
        with self.assertRaisesRegex(FileNotFoundError, 'File /path/to/file not found in mock function'):
            with open('/path/to/file'):
                pass

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_return_new_mock_when_defaults_mock_and_file_not_registered(self, open_mock):
        # given
        open_mock.default_behavior = DEFAULTS_MOCK

        # when
        with open('/path/to/file') as f:
            result = f

        # then
        self.assertIsInstance(result, MagicMock)

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_use_the_same_mock_when_called_twice(self, open_mock):
        # given
        open_mock.default_behavior = DEFAULTS_MOCK

        # when
        with open('/path/to/file') as f:
            result = f

        with open_mock('/path/to/file') as x:
            result2 = x

        # then
        self.assertIsInstance(result, MagicMock)
        self.assertIs(result, result2)
        saved_mock = open_mock.get_object_for_path('/path/to/file')
        self.assertEqual(saved_mock.__enter__.call_count, 2)
        self.assertEqual(saved_mock.__exit__.call_count, 2)

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_raise_exception_when_defaults_original_and_file_not_registered_and_file_not_exists(self, open_mock):
        # given
        open_mock.default_behavior = DEFAULTS_ORIGINAL

        # when
        with self.assertRaisesRegex(FileNotFoundError, "No such file or directory: '/path/to/file'"):
            with open('/path/to/file'):
                pass

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_return_original_fle_when_defaults_mock_and_file_not_registered(self, open_mock):
        # given
        open_mock.default_behavior = DEFAULTS_ORIGINAL
        file_path = join(dirname(test_module.__file__), 'data', 'example_data.txt')
        expected_content = 'some example\nDATA\n123'

        # when
        with open(file_path) as f:
            result = f.read()

        # then
        self.assertEqual(result, expected_content)

    @patch('io.open', new_callable=MockOpen)
    def test_should_return_original_fle_when_defaults_mock_and_file_not_registered_and_io_open_patched(self, open_mock):
        # given
        open_mock.default_behavior = DEFAULTS_ORIGINAL
        file_path = join(dirname(test_module.__file__), 'data', 'example_data.txt')
        expected_content = 'some example\nDATA\n123'

        # when
        with io.open(file_path) as f:
            result = f.read()

        # then
        self.assertEqual(result, expected_content)

    @patch('io.open', new_callable=MockOpen)
    @patch('builtins.open', new_callable=MockOpen)
    def test_raise_exception_when_open_and_io_open_patched_with_io_open(self, open_mock, ioopen_mock):
        # given
        ioopen_mock.default_behavior = DEFAULTS_ORIGINAL
        file_path = join(dirname(test_module.__file__), 'data', 'example_data.txt')

        # when
        with self.assertRaisesRegex(RuntimeError, 'Both open and io.open already patched'):
            with io.open(file_path):
                pass

    @patch('io.open', new_callable=MockOpen)
    @patch('builtins.open', new_callable=MockOpen)
    def test_raise_exception_when_open_and_io_open_patched_with_open(self, open_mock, ioopen_mock):
        # given
        open_mock.default_behavior = DEFAULTS_ORIGINAL
        file_path = join(dirname(test_module.__file__), 'data', 'example_data.txt')

        # when
        with self.assertRaisesRegex(RuntimeError, 'Both open and io.open already patched'):
            with open(file_path):
                pass

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_return_original_file_and_registered_object(self, open_mock):
        # given
        open_mock.default_behavior = DEFAULTS_ORIGINAL
        custom_obj = self.CustomObj()
        non_mocked_path = join(dirname(test_module.__file__), 'data', 'example_data.txt')
        open_mock.register_object_for_path(path='/path/to/file', obj=custom_obj)
        expected_mock_content = 'some example\nDATA\n123'

        # when
        with open(non_mocked_path) as f:
            result1 = f.read()

        with open('/path/to/file') as x:
            result2 = x.read()

        # then
        self.assertEqual(result1, expected_mock_content)
        self.assertEqual(result2, 'read')

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_raise_exception_when_file_not_found_and_invalid_behavior(self, open_mock):
        # given
        open_mock.default_behavior = 'InvalidBehavior'

        # when
        with self.assertRaisesRegex(ValueError, 'InvalidBehavior is not valid default behavior'):
            with open('/path/to/file'):
                pass

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_raise_exception_when_path_registered_twice(self, open_mock):
        # given
        open_mock.register_object_for_path('/path/to/file', 'ABC')

        # when
        with self.assertRaisesRegex(ValueError, 'Path /path/to/file already registered with object ABC'):
            open_mock.register_object_for_path('/path/to/file', 'XYZ')

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_update_registered_object(self, open_mock):
        # when
        open_mock.register_object_for_path('/path/to/file', 'ABC')

        # then
        self.assertEqual(open_mock.get_object_for_path('/path/to/file'), 'ABC')

        # when
        open_mock.update_object_for_path('/path/to/file', 'XYZ')

        # then
        self.assertEqual(open_mock.get_object_for_path('/path/to/file'), 'XYZ')

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_remove_registered_object(self, open_mock):
        # when
        open_mock.register_object_for_path('/path/to/file', 'ABC')

        # then
        self.assertEqual(open_mock.get_object_for_path('/path/to/file'), 'ABC')

        # when
        open_mock.unregister_path('/path/to/file')

        # then
        with self.assertRaisesRegex(KeyError, '/path/to/file'):
            open_mock.get_object_for_path('/path/to/file')

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_register_data_file(self, open_mock):
        # given
        return_data = 'Some data\nin file'
        open_mock.set_read_data_for('/path/to/file', return_data)

        # when
        with open_mock('/path/to/file') as f:
            result = f.read()

        # then
        self.assertEqual(result, return_data)

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_register_data_file_without_context_manager(self, open_mock):
        # given
        return_data = 'Some data\nin file'
        open_mock.set_read_data_for('/path/to/file', return_data)

        # when
        f = open_mock('/path/to/file')
        result = f.read()

        # then
        self.assertEqual(result, return_data)

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_raise_exception_when_register_data_for_existing_path_mapping(self, open_mock):
        # given
        return_data = 'Some data\nin file'
        open_mock.register_object_for_path('/path/to/file', 'ABC')

        # when
        with self.assertRaisesRegex(ValueError, 'Path /path/to/file already registered with object ABC'):
            open_mock.set_read_data_for('/path/to/file', return_data)

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_open_original_file_in_binary_mode(self, open_mock):
        # given
        open_mock.default_behavior = DEFAULTS_ORIGINAL
        path = join(dirname(test_module.__file__), 'data', 'example_data.txt')

        # when
        with open(path, 'rb') as f:
            result = f.read()

        # then
        self.assertIsInstance(result, bytes)

    @patch('builtins.open', new_callable=MockOpen)
    def test_should_open_original_file_for_write(self, open_mock):
        # given
        open_mock.default_behavior = DEFAULTS_ORIGINAL
        tempfile = mkstemp(prefix='mock_open_file_unit_test_')[1]

        # when
        with open(tempfile, mode='w') as f:
            f.write('QWERTY')

        with open_mock(tempfile) as f:
            result = f.read()

        # then
        self.assertEqual(result, 'QWERTY')

        # cleanup
        unlink(tempfile)
