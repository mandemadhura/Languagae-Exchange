impoiirt importlib
import os
import sys
from pathlib import Path

from lang_exch.setup.setup import config


class DBFactory:
    '''singleton factory class for database instantiation'''

    def __new__(cls, _db_name=None):
        '''static new method'''
        cls._db_name = _db_name
        if not hasattr(cls, '_db_instance'):
            cls._db_instance = cls.get_instance(cls._db_name)
        return cls._db_instance

    def get_instance(db_name):
        '''Returns an instance of a database provider'''
        pwd = os.getcwd()
        req_path = None
        _db_instance = None

        # Get the provider module like 'PostgresDB'.
        # Dont hardcode it
        for path in sys.path:
            if pwd in path:
                req_path = path
                break

        if req_path:
            # get the PosixPath
            db_path = Path(req_path)
            if db_path.exists():
                # There is a way to iterate posixpath dir using iterdir()
                # But facing one problem after one iteration. Hence, iterating
                # using os.listdir()
                for pkg in os.listdir(db_path):
                    if not os.path.isdir(pkg) and db_name in pkg:
                        module = importlib.import_module(pkg.split('.')[0])
                        db_attribute = getattr(module, 'PostgresDB', None)
                        if db_attribute is not None:
                            _db_instance = db_attribute(db_config = dict(config._sections['database']))
                            break
        return _db_instance

if __name__ == '__main__':
    import pdb
    # pdb.set_trace()
    db = DBFactory('postgres')
    db = DBFactory('postgres')
