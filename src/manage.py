#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def run_django_admin():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoflix.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Ensure it's installed and available on your PYTHONPATH. "
            "Did you forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    run_django_admin()
