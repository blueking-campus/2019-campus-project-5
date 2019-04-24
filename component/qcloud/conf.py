# -*- coding: utf-8 -*-
import importlib
from .utils import get_current_environ


# 动态更新globals命名空间
module = importlib.import_module('.sites.%(env)s.conf' % {
                                 'env': get_current_environ()}, package=__package__)

for variable in getattr(module, '__all__', []):
    globals()[variable] = getattr(module, variable)
