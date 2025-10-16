"""Backend package.

This package contains backend-local implementations (`config_impl`, `models_impl`) and a
shim `api.py` that wires them together. It provides stable package import paths during
the reorganization process.
"""

from . import api as api
from . import models as models
from . import config as config

__all__ = ["api", "models", "config"]
