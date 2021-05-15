import importlib
import os
import sys
from pathlib import Path


class DBFactory:
    '''singleton factory class for database instantiation'''

    def __new__(cls, _db_name=None):
        '''static new method'''
        cls._db_name = _db_name
        if not hasattr(cls, '_db_instance'):
            cls._db_instance = cls.get_instance(cls._db_name)
        return cls._db_instance

    def get_instance(db_name):
        pwd = os.getcwd()
        req_path = None
        _db_instance = None

        for path in sys.path:
            if pwd in path:
                req_path = path
                break

        if req_path:
            q = Path(req_path)
            if q.exists():
                for pkg in os.listdir(q):
                    if db_name in pkg:
                        module = importlib.import_module(pkg.split('.')[0])
                        db_attribute = getattr(module, 'PostgresDB', None)
                        if db_attribute is not None:
                            _db_instance = db_attribute('localhost', 'le_user', 'lang_exch')
                            break
        return _db_instance

if __name__ == '__main__':
    import pdb
    # pdb.set_trace()
    db = DBFactory('postges')
    db = DBFactory('postges')
