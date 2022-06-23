from lang_exch.conf.log.lang_exch_logging import logger
from inspect import stack
import inspect


class BaseError(Exception):
    """Parent class for language-exchange error"""
    _rc = 0
    _desc = ""
    _caller = ""
    
    def __init__(self, rc=0, message=None):
        """Initialization"""
        super(BaseError, self).__init__()
        self._rc = rc
        self._desc = message
        self._caller = inspect.stack()[1][3]
      
    @property
    def caller(self):
        return self._caller
    
    @property
    def desc(self):
        return self._desc
    
    @property
    def rc(self):
        return self._rc
    
    def __repr__(self) -> str:
        return f"{self.caller}: {self.desc}: {self.rc}"
    
    
class languageNotValidError(BaseError):
    """Handles language invalid errors"""
    
    def __init__(self, rc=0, msg='Language name is not valid'):
        super().__init__(rc, message=msg)
        logger.error(f"error: {self.caller}: {self._desc} {self.rc}")
        