__author__ = 'Skye.Tang 2017-10-28'

class _const(object):
    class ConstError(PermissionError):pass
    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name]=value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise  self.ConstError("Can't unbind const(%s)" % name)
        raise  NameError(name)

import sys
sys.modules[__name__]=_const()

_const.kError = "kError"