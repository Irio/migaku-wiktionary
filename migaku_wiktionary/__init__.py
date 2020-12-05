import sys

import progressbar


def is_in_test_environment():
    return "pytest" in sys.modules


if is_in_test_environment():
    ProgressBar = progressbar.NullBar
else:
    ProgressBar = progressbar.ProgressBar
