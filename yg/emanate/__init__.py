# -*- coding: utf-8 -*-
from .events import Event

__author__ = 'YouGov, plc'
__email__ = 'dev@yougov.com'

__all__ = ['Event']

try:
    import pkg_resources
    dist = pkg_resources.get_distribution('yg.emanate')
    __version__ = dist.version
except Exception:
    __version__ = 'unknown'
