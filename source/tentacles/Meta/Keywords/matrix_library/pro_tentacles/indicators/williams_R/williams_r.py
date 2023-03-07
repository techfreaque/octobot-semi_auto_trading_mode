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


async def get_williams_R(maker, indicator, evaluator):
    length = await user_input2(maker, indicator, "Williams %R length", "int", 50, 0)
    await allow_enable_plot(maker, indicator, "Plot Williams %R")
    data = tulipy.willr(
        await get_candles_(maker, "high"),
        await get_candles_(maker, "low"),
        await get_candles_(maker, "close"),
        length,
    )
    data_source = {
        "v": {
            "title": f"Williams %R {length}",
            "data": data,
            "chart_location": "main-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_source)
