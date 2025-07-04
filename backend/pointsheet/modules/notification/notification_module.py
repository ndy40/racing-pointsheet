"""
Notification module for the pointsheet application.

This module provides webhook notification functionality for various events in the application.
"""
import importlib

from lato import ApplicationModule

notification_module = ApplicationModule("notification_module")
importlib.import_module("modules.notification.handlers")
