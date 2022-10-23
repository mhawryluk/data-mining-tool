from .automate_steps import AutomateSteps


def format_set(set_: tuple):
    return f"{{{',  '.join(set_)}}}"
