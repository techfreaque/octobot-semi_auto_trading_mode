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

import typing
from tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords import (
    user_inputs2,
)
from tentacles.Meta.Keywords.matrix_library.pro_tentacles.indicators import (
    supported_indicators,
)
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.indicators.indicators_base as indicators_base


async def get_configurable_indicator(maker, evaluator, indicator_id: int = 1):
    indicator: indicators_base.Indicator = evaluator.indicators[indicator_id]
    return await indicator.get_indicator_data(maker, evaluator=evaluator)


async def activate_configurable_indicator(
    maker,
    evaluator,
    data_source_name="Data Source",
    def_val="EMA",
    indicator_id=1,
    enable_oscillators=True,
    enable_price_indicators=True,
    enable_price_data=True,
    enable_volume=True,
    enable_static_value=True,
    enable_force_def_val=False,
    enable_multi_data_indicators=False,
):
    indicator = indicators_base.Indicator()
    await indicator.init_indicator(
        maker=maker,
        evaluator=evaluator,
        data_source_name=data_source_name,
        def_val=def_val,
        indicator_id=indicator_id,
        enable_oscillators=enable_oscillators,
        enable_price_indicators=enable_price_indicators,
        enable_price_data=enable_price_data,
        enable_volume=enable_volume,
        enable_static_value=enable_static_value,
        enable_force_def_val=enable_force_def_val,
        enable_multi_data_indicators=enable_multi_data_indicators,
    )
    maker.indicators[indicator.cache_path] = evaluator.indicators[
        indicator_id
    ] = indicator
    return evaluator.indicators[indicator_id].indicator_name


async def get_configurable_indicators(maker, evaluator, indicator_ids: list) -> list:
    indicators_data = []
    for indicator_id in indicator_ids:
        indicator: indicators_base.Indicator = evaluator.indicators[indicator_id]
        indicators_data.append(
            await indicator.get_indicator_data(maker, evaluator=evaluator)
        )
    return indicators_data


async def activate_multiple_configurable_indicators(
    maker,
    evaluator,
    data_source_name: str = "Data Source",
    def_val: list = ["EMA"],
    indicator_group_id: int = 1,
    enable_oscillators: bool = True,
    enable_price_indicators: bool = True,
    enable_price_data: bool = True,
    enable_volume: bool = True,
    enable_static_value: bool = True,
    enable_force_def_val: bool = False,
) -> typing.Tuple[list, list]:
    if enable_force_def_val:
        indicator_names = def_val
    else:
        available_sources = supported_indicators.get_supported_indicators_(
            enable_oscillators=enable_oscillators,
            enable_price_indicators=enable_price_indicators,
            enable_static_value=enable_static_value,
            enable_price_data=enable_price_data,
        )
        indicator_names = await user_inputs2.user_input2(
            maker,
            evaluator,
            f"select_{data_source_name}",
            "multiple-options",
            def_val=def_val,
            title=f"Select {data_source_name}",
            options=available_sources,
        )
    selected_indicator_names: list = []
    selected_indicator_ids: list = []
    for index, indicator_name in enumerate(indicator_names):
        this_data_source_name = f"{data_source_name} {index}"
        this_indicator_id = index + indicator_group_id + 10
        indicator_name = await activate_configurable_indicator(
            maker=maker,
            evaluator=evaluator,
            data_source_name=this_data_source_name,
            def_val=indicator_name,
            indicator_id=this_indicator_id,
            enable_oscillators=enable_oscillators,
            enable_price_indicators=enable_price_indicators,
            enable_price_data=enable_price_data,
            enable_volume=enable_volume,
            enable_static_value=enable_static_value,
            enable_force_def_val=True,
        )
        selected_indicator_names.append(indicator_name)
        selected_indicator_ids.append(this_indicator_id)
    return selected_indicator_names, selected_indicator_ids
