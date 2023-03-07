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

import tulipy
from tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
)
from tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)


async def get_Aroon(maker, indicator, evaluator):
    length = await user_input2(maker, indicator, "Aroon length", "int", 10)
    await allow_enable_plot(maker, indicator, "plot Aroon")
    aroon_down, aroon_up = tulipy.aroon(
        await get_candles_(maker, "low"), await get_candles_(maker, "high"), length
    )
    data = {
        "v": {
            "title": f"Aroon Down ({length})",
            "data": aroon_down,
            "chart_location": "sub-chart",
        },
        "u": {
            "title": f"Aroon UP ({length})",
            "data": aroon_up,
            "chart_location": "sub-chart",
        },
    }
    return await store_indicator_data(maker, indicator, data)
