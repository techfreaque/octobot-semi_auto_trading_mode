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


async def get_heikin_ashi(maker, indicator, evaluator):
    source = await user_input2(
        maker,
        indicator,
        "select heikin ashi source",
        "options",
        "Heikin Ashi close",
        options=[
            "Heikin Ashi open",
            "Heikin Ashi high",
            "Heikin Ashi low",
            "Heikin Ashi close",
        ],
    )
    await allow_enable_plot(maker, indicator, "Plot Heikin Ashi")
    data_source = {
        "v": {
            "title": f"{source}",
            "data": await get_candles_(maker, source),
            "chart_location": "main-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_source)
