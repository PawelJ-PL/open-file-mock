Open File Mock
==============

Description
-----------

This library contains object, which can be used during mocking files in
tests. Features:

-  You can register different actions (provide different objects) for
   different paths
-  You can add text, which will be returned on read
-  You can select behavior for paths, which are not registered.
   Supported behaviors:

   -  Raise FileNotFoundError exception (default behavior)
   -  Return original file from filesystem
   -  Return mock object

Install
-------

It can be installed with following command:

``pip install open-mock-file``

Usage:
------

Examples
~~~~~~~~

Mock open first file with custom object, second one with string data and
raise FileNotFoundError for not registered path:

.. code:: python

    from unittest.mock import patch
    from open_file_mock import MockOpen


    class FileObject:
        def __init__(self, data):
            self.data = data

        def read(self, *args, **kwargs):
            return self.data

        def write(self, data, *args, **kwargs):
            self.data = data

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass


    with patch('builtins.open', new_callable=MockOpen) as open_mock:
        open_mock.register_object_for_path(path='/tmp/f1', obj=FileObject('Some data'))
        open_mock.set_read_data_for(path='/tmp/f2', data='file2 data')
        with open('/tmp/f1') as f1:
            print(f1.read())
            f1.write('Other data')
            print(f1.read())
            print('----------------------')

        with open('/tmp/f2') as f2:
            print(f2.read())
            print('----------------------')

        open('/etc/hostname')

**output:**

::

    Some data
    Other data
    ----------------------
    file2 data
    ----------------------
    Traceback (most recent call last):
    ...
    FileNotFoundError: File /etc/hostname not found in mock function

Set default behavior (for not registered paths) to return original file:

.. code:: python

    from unittest.mock import patch, MagicMock
    from open_file_mock import MockOpen, DEFAULTS_ORIGINAL

    with patch('builtins.open', new_callable=MockOpen) as open_mock:
        open_mock.default_behavior = DEFAULTS_ORIGINAL
        open_mock.register_object_for_path(path='/tmp/f1', obj=MagicMock())
        with open('/tmp/f1') as f1:
            print(f1.read())
            print('----------------------')

        with open('/etc/hostname') as f2:
            print(f2.read())
            print('----------------------')

**output:**

::

    <MagicMock name='mock.__enter__().read()' id='...'>
    ----------------------
    myhost

    ----------------------

Set default behavior to return new mock:

.. code:: python

    from unittest.mock import patch
    from open_file_mock import MockOpen, DEFAULTS_MOCK

    with patch('builtins.open', new_callable=MockOpen) as open_mock:
        open_mock.default_behavior = DEFAULTS_MOCK
        open_mock.set_read_data_for('/tmp/f1', 'QWERTY')
        with open('/tmp/f1') as f1:
            print(f1.read())
            print('----------------------')

        with open('/etc/hostname') as f2:
            print(f2.read())
            print('----------------------')

**output:**

::

    QWERTY
    ----------------------
    <MagicMock name='mock.__enter__().read()' id='...'>
    ----------------------

Yoy can get registered object with *get\_object\_for\_path* method:

.. code:: python

    from unittest.mock import patch
    from open_file_mock import MockOpen


    class FileObject:
        def __init__(self, data):
            self.data = data

        def read(self, *args, **kwargs):
            return self.data

        def write(self, data, *args, **kwargs):
            self.data = data

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass


    with patch('builtins.open', new_callable=MockOpen) as open_mock:
        open_mock.register_object_for_path(path='/tmp/f1', obj=FileObject('Some data'))
        open_mock.set_read_data_for(path='/tmp/f2', data='file2 data')
        with open('/tmp/f1') as f1:
            print(f1.read())
            print('----------------------')

        print(open_mock.get_object_for_path('/tmp/f1'))

**output:**

::

    Some data
    ----------------------
    <__main__.FileObject object at ...>

Object methods:
~~~~~~~~~~~~~~~

-  **register\_object\_for\_path(path, obj)** - allow to register new
   object for provided path. Can be used once for particular path
-  **update\_object\_for\_path(path, obj)** - update registered path or
   create new mapping if not exists
-  **unregister\_path(path)** - remove path mapping
-  **set\_read\_data\_for(path, data)** - set data which will be
   returned of file read
-  **get\_object\_for\_path(path)** - returns object registered for
   path. If mapping not exists, raises KeyError
