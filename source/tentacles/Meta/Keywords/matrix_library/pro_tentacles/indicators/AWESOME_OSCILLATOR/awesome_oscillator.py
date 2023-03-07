import tulipy
from tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.data.public_exchange_data import (
    get_candles_,
)
from tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.indicator_keywords.plotting import (
    store_indicator_data,
    allow_enable_plot,
)


async def get_awesome_oscillator(maker, indicator, evaluator):
    await allow_enable_plot(maker, indicator, "Plot awesome_oscillator")
    data = tulipy.ao(
        await get_candles_(maker, "high"), await get_candles_(maker, "low")
    )
    data_source = {
        "v": {
            "title": "awesome_oscillator",
            "data": data,
            "chart_location": "sub-chart",
        }
    }
    return await store_indicator_data(maker, indicator, data_source)
