# coding=utf8
"""
信号
"""

from django.dispatch import Signal, receiver

from library.log import logger


class SignalDefaultSender(object):
    """
    默认信号sender
    """
    pass


SIGNAL_DEFAULT_SENDER = SignalDefaultSender()

# test
signal_test = Signal()


@receiver(signal_test)
def execute_signal_test(sender, **kwargs):
    """
    test
    :param sender:
    :param kwargs:
    :return:
    """
    logger.info("execute_signal_test")
