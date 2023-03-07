# a42.ch CONFIDENTIAL
# __________________
#
#  [2021] - [∞] a42.ch Incorporated
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of a42.ch Incorporated and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to a42.ch Incorporated
# and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from a42.ch Incorporated.
#
# If you want to use any code for commercial purposes,
# or you want your own custom solution,
# please contact me at max@a42.ch

import subprocess
import sys


class MissingThirdPartyPackageError(Exception):
    pass


def raise_missing_third_party_package_missing_error(module_name, _error):
    raise MissingThirdPartyPackageError(
        f"failed to install {module_name} - "
        "install it manually to use Matrix-Pro-Tentacles"
    ) from _error


try:
    import pandas as _
except (ImportError, ModuleNotFoundError):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    except Exception as error:
        raise_missing_third_party_package_missing_error("pandas", error)
try:
    import pandas_ta as _
except (ImportError, ModuleNotFoundError):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas_ta"])
    except Exception as error:
        raise_missing_third_party_package_missing_error("pandas_ta", error)
try:
    import finta as _
except (ImportError, ModuleNotFoundError):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "finta"])
    except Exception as error:
        raise_missing_third_party_package_missing_error("finta", error)
try:
    import tulipy as _
except (ImportError, ModuleNotFoundError):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tulipy"])
    except Exception as error:
        raise_missing_third_party_package_missing_error("tulipy", error)
try:
    import statistics as _
except (ImportError, ModuleNotFoundError):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "statistics"])
    except Exception as error:
        raise_missing_third_party_package_missing_error("statistics", error)
