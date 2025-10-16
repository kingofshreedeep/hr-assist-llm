"""Entrypoint to run the Streamlit app from the `frontend/` folder.
This module imports the top-level `app` module (keeps existing logic intact) and
serves as the target for `streamlit run frontend/app_main.py`.
"""
from importlib import import_module

# Importing the original top-level Streamlit app module so its code executes
import_module('app')
