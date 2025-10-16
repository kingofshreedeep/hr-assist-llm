"""Shim frontend.app that simply imports the top-level Streamlit app module.
This file is used by the updated run.sh to run the Streamlit app via package path.
"""
from importlib import import_module

_app = import_module('app')

# Nothing else needed; Streamlit will execute the module when invoked
