# -*- coding: UTF-8 -*-
"""
账号体系的简单工厂，提供静态工厂方法根据环境返回账号子类对象
"""
from account.settings_account import RUN_VER
from account.settings_account import logger


class AccountFactory(object):
    """
    账号体系的简单工厂，提供静态工厂方法根据环境返回账号子类对象
    """
    @staticmethod
    def getAccountObj():
        # 根据环境确定模块名
        className = RUN_VER.strip().capitalize() + "Account"
        fileName = RUN_VER + '_account'
        moduleName = "account.%s.%s" % (RUN_VER, fileName)
        try:
            module = __import__(moduleName, globals(), locals(), [className])
            cls = getattr(module, className)
            return cls()    # 账号类都是单例， 所以不会有多次创建对象的问题
        except Exception, e:
            logger.error(u"加载%s环境下%s类失败，异常信息：%s" % (RUN_VER, moduleName, e))
            raise e
