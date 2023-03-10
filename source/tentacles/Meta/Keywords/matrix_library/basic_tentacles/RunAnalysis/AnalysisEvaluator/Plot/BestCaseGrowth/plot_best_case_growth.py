#  Drakkar-Software OctoBot-Trading
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

from tentacles.Meta.Keywords.matrix_library.basic_tentacles.RunAnalysis.BaseDataProvider.default_base_data_provider import (
    base_data_provider,
)


async def plot_best_case_growth(
    run_data: base_data_provider.RunAnalysisBaseDataGenerator,
    plotted_element,
    x_as_trade_count: bool = False,
    own_yaxis: bool = False,
):
    await run_data.get_best_case_growth_from_transactions(
        x_as_trade_count,
    )
    plotted_element.plot(
        mode="scatter",
        x=run_data.best_case_growth_x_data,
        y=run_data.best_case_growth_data,
        x_type="tick0" if x_as_trade_count else "date",
        title="best case growth",
        own_yaxis=own_yaxis,
        line_shape="hv",
    )
