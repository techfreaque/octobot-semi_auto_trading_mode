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

from octobot_trading.api.exchange import (
    get_all_exchange_ids_from_matrix_id,
    get_exchange_managers_from_exchange_ids,
)
from tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.tools.utilities import (
    cut_data_to_same_len,
)
from tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.user_inputs2 import (
    user_input2,
)
from tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
    user_select_candle_source_name,
)
from tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)


async def get_exchange_delta(maker, indicator, evaluator):
    matrix_id = maker.ctx.matrix_id
    exchange_ids = get_all_exchange_ids_from_matrix_id(matrix_id)
    exchange_managers = get_exchange_managers_from_exchange_ids(exchange_ids)
    exchanges = [
        exchange_manager.exchange_name for exchange_manager in exchange_managers
    ]
    candle_source_name = await user_select_candle_source_name(
        maker, indicator, "Select Candle Source"
    )
    from_exchange = await user_input2(
        maker, indicator, "From exchange", "options", exchanges[0], options=exchanges
    )
    plot_precent = await user_input2(
        maker,
        indicator,
        "Plot percent insted of prices",
        "boolean",
        True,
    )
    to_exchange = await user_input2(
        maker, indicator, "To exchange", "options", exchanges[-1], options=exchanges
    )
    await allow_enable_plot(maker, indicator, "Plot exchange delta")
    from_closes = None
    to_closes = None
    try:
        for exchange_manager in exchange_managers:
            if from_exchange == exchange_manager.exchange_name:
                from_closes = await get_candles_(
                    exchange_manager.trading_modes[0].producers[0],
                    candle_source_name,
                    time_frame=maker.ctx.time_frame,
                    symbol=maker.ctx.symbol,
                )
            if to_exchange == exchange_manager.exchange_name:
                to_closes = await get_candles_(
                    exchange_manager.trading_modes[0].producers[0],
                    candle_source_name,
                    time_frame=maker.ctx.time_frame,
                    symbol=maker.ctx.symbol,
                )

        from_closes, to_closes = cut_data_to_same_len((from_closes, to_closes))
        if plot_precent:
            delta_data = (from_closes - to_closes) / (from_closes / 100)
        else:
            delta_data = from_closes - to_closes
        data_source = {
            "v": {
                "title": f" candle {candle_source_name} delta from {from_exchange} to {to_exchange}",
                "data": delta_data,
                "chart_location": "sub-chart",
            },
            "f": {
                "title": f"{from_exchange} {candle_source_name} price",
                "data": from_closes,
                "chart_location": "main-chart",
            },
            "t": {
                "title": f"{to_exchange} {candle_source_name} price",
                "data": to_closes,
                "chart_location": "main-chart",
            },
        }
    except (AttributeError, TypeError):
        data_source = {
            "v": {
                "title": f" candle {candle_source_name} delta from {from_exchange} to {to_exchange}",
                "data": [0],
                "chart_location": "sub-chart",
            },
            "f": {
                "title": f"{from_exchange} {candle_source_name} price",
                "data": [0],
                "chart_location": "main-chart",
            },
            "t": {
                "title": f"{to_exchange} {candle_source_name} price",
                "data": [0],
                "chart_location": "main-chart",
            },
        }
        maker.logger.info(
            "Plot exchange delta is not possible. Other exchange is not initialized - this is normal if you just started octobot"
        )
    return await store_indicator_data(maker, indicator, data_source)
