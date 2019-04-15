from __future__ import annotations

import typing

from .. import types
from ..types import base
from ..utils.mixins import DataMixin, ContextInstanceMixin
from ..utils.payload import generate_payload, prepare_arg


class Bot(DataMixin, ContextInstanceMixin):
    """
    Base bot class
    """
    pass
