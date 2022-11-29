from .automate_steps import AutomateSteps
from .QImage import QImage
from .QtImageViewer import QtImageViewer


def format_set(set_: tuple):
    return f"{{{',  '.join(set_)}}}"
