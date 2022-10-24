from .automate_steps import AutomateSteps
from .QtImageViewer import QtImageViewer
from .QImage import QImage


def format_set(set_: tuple):
    return f"{{{',  '.join(set_)}}}"
