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

import numpy as numpy
import octobot_commons.enums as commons_enums
import tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.data.public_exchange_data as public_exchange_data
import tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.user_inputs2 as user_inputs2
import tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.data.write_evaluator_cache as write_evaluator_cache
import tentacles.Meta.Keywords.scripting_library.data.writing.plotting as _plotting


async def store_indicator_plots(
    maker,
    config_path,
    main_data,
    additional_values_by_key: dict = {},
    enable_rounding=True,
    filter_nan_for_plots=False,
):
    if maker.ctx.exchange_manager.is_backtesting or (
        not maker.ctx.exchange_manager.is_backtesting and not maker.live_recording_mode
    ):
        await write_evaluator_cache.store_indicator_history(
            maker,
            main_data,
            value_key=config_path + "v",
            additional_values_by_key=additional_values_by_key,
            enable_rounding=enable_rounding,
            filter_nan_for_plots=filter_nan_for_plots,
        )
    else:
        if not filter_nan_for_plots or str(main_data[-1]) != str(numpy.nan):
            await maker.ctx.set_cached_value(main_data[-1], config_path + "lv")
        for value_key in additional_values_by_key:
            if not filter_nan_for_plots or str(
                additional_values_by_key[value_key][-1]
            ) != str(numpy.nan):
                await maker.ctx.set_cached_value(
                    additional_values_by_key[value_key][-1], value_key
                )


async def store_and_plot_indicator(
    maker,
    indicator,
    title,
    value_key,
    main_data,
    chart_location="main-chart",
    mode="lines",
    line_shape="linear",
    enable_rounding=True,
):
    if indicator.plot:
        _value_key = indicator.config_path_short + value_key
        if maker.ctx.exchange_manager.is_backtesting or (
            not maker.ctx.exchange_manager.is_backtesting
            and not maker.live_recording_mode
        ):
            _value_key += "v"
            await write_evaluator_cache.store_indicator_history(
                maker,
                main_data,
                value_key=_value_key,
                enable_rounding=enable_rounding,
            )
        else:
            _value_key += "lv"
            await maker.ctx.set_cached_value(main_data[-1], _value_key)

        await _plotting.plot(
            maker.ctx,
            title,
            cache_value=_value_key,
            chart=chart_location,
            mode=mode,
            line_shape=line_shape,
        )


async def store_indicator_data(
    maker,
    indicator,
    data,
    force_plot_disable=False,
    own_yaxis=False,
    enable_rounding=True,
    filter_nan_for_plots=False,
):
    indicator.data = {"time_frame": indicator.time_frame}
    additional_values_by_key = {}
    main_data = None
    for value_key in data:
        data[value_key]["data"] = await normalize_any_time_frame_to_this_time_frame(
            maker,
            data[value_key]["data"],
            indicator.time_frame,
            maker.ctx.time_frame,
        )
        if indicator.plot and not force_plot_disable:
            if value_key == "v":
                main_data = data[value_key]["data"]
            else:
                _value_key = (
                    indicator.config_path_short + "l" + value_key
                    if maker.live_recording_mode
                    else indicator.config_path_short + value_key
                )
                additional_values_by_key[_value_key] = data[value_key]["data"]
        indicator.data[value_key] = data[value_key]
        if len(data[value_key]["data"]) == 0:
            indicator.plot = False
            maker.ctx.logger.error(
                f"Data Source: {data[value_key]['title']} data is empty"
                " check Candles history size. "
            )
    if indicator.plot and not force_plot_disable:
        await store_indicator_plots(
            maker,
            indicator.config_path_short,
            main_data,
            additional_values_by_key,
            enable_rounding=enable_rounding,
            filter_nan_for_plots=filter_nan_for_plots,
        )
        for index, value_key in enumerate(data):
            _value_key = (
                indicator.config_path_short + "l" + value_key
                if maker.live_recording_mode
                else indicator.config_path_short + value_key
            )
            await _plotting.plot(
                maker.ctx,
                data[value_key]["title"],
                cache_value=_value_key,
                chart=data[value_key].get("chart_location", "main-chart"),
                color="red",
                own_yaxis=own_yaxis if index == 0 else False,
                mode=data[value_key].get("mode", None),
                line_shape=data[value_key].get("line_shape", None),
            )
    return indicator.data


async def normalize_any_time_frame_to_this_time_frame(
    maker,
    data,
    source_time_frame: str,
    target_time_frame: str,
):
    target_time_frame_timestamps: list = await public_exchange_data.get_candles_(
        maker, "time", time_frame=target_time_frame
    )
    source_time_frame_timestamps: list = await public_exchange_data.get_candles_(
        maker, "time", time_frame=source_time_frame
    )

    if source_time_frame == target_time_frame:
        return data
    # different time frame as trigger timeframe
    data_time_frame_minutes = commons_enums.TimeFramesMinutes[
        commons_enums.TimeFrames(source_time_frame)
    ]
    target_time_frame_minutes = commons_enums.TimeFramesMinutes[
        commons_enums.TimeFrames(target_time_frame)
    ]
    candles_to_add = data_time_frame_minutes / target_time_frame_minutes

    index = 1
    unified_data = []
    if candles_to_add > 0:
        # target timeframe is smaller
        for index in range(1, len(target_time_frame_timestamps)):
            if source_time_frame_timestamps[-1] == target_time_frame_timestamps[-index]:
                break
            unified_data.insert(0, data[-1])
            index += 1
    else:
        # target timeframe is bigger
        raise NotImplementedError(
            "Indicator timeframe must be gretaer or equal to the trigger timeframe"
        )

    origin_data_len = len(data)
    target_data_len = len(target_time_frame_timestamps)
    data_index = 2
    try:
        if candles_to_add > 0:
            # target timeframe is smaller
            while index <= target_data_len and origin_data_len >= data_index:
                virtual_candle_index = 1
                while (
                    (virtual_candle_index <= candles_to_add)
                    and index <= target_data_len
                    and origin_data_len >= data_index
                ):
                    virtual_candle_index += 1
                    unified_data.insert(0, data[-data_index])
                    index += 1
                data_index += 1
        else:
            # target timeframe is bigger
            while index <= target_data_len:
                pass
        return unified_data
    except Exception as error:
        raise RuntimeError(
            f"Failed to adapt indicator from {source_time_frame} to {target_time_frame}"
        ) from error


async def store_evaluator_plots(
    maker, values, signals, second_values=None
):  # , additional_values_by_key=None):
    if maker.ctx.exchange_manager.is_backtesting or (
        not maker.ctx.exchange_manager.is_backtesting and not maker.live_recording_mode
    ):
        data_length = len(signals)
        times = await public_exchange_data.get_candles_(maker, "time")
        times = times[-data_length:]
        if second_values:
            second_values = second_values[-data_length:]
        y_cache = []
        y_cache_second = []
        y_times = []
        indicator_values = values[-data_length:]
        for index, signal in enumerate(signals):
            if signal:
                y_cache.append(indicator_values[index])
                y_times.append(times[index])
                if second_values:
                    y_cache_second.append(second_values[index])
        additional_cache = (
            {
                maker.strategies[maker.current_strategy_id]
                .evaluators[maker.current_evaluator_id]
                .config_path_short
                + "v2": y_cache_second
            }
            if second_values
            else {}
        )

        await maker.ctx.set_cached_values(
            values=y_cache,
            cache_keys=y_times,
            value_key=maker.strategies[maker.current_strategy_id]
            .evaluators[maker.current_evaluator_id]
            .config_path_short
            + "v",
            additional_values_by_key=additional_cache,
        )
    else:
        try:
            signals = signals[-1]
        except (IndexError, KeyError, TypeError):
            # its a single signal
            pass
        if signals == 1:
            _value_key = (
                maker.strategies[maker.current_strategy_id]
                .evaluators[maker.current_evaluator_id]
                .config_path_short
                + "lv"
                if maker.live_recording_mode
                else maker.strategies[maker.current_strategy_id]
                .evaluators[maker.current_evaluator_id]
                .config_path_short
                + "v"
            )
            await maker.ctx.set_cached_value(values[-1], _value_key)
            if second_values:
                await maker.ctx.set_cached_value(second_values[-1], _value_key + "2")


async def store_evaluator_data(maker, evaluator, allow_signal_extension=False):
    if allow_signal_extension:
        evaluator.signal_valid_for = await user_inputs2.user_input2(
            maker, evaluator, "extend signal X candles", "int", 0
        )
        if evaluator.signal_valid_for != 0:
            signals = []
            for index, signal in enumerate(evaluator.signals):
                if signal == 1:
                    signals.append(signal)
                else:
                    try:
                        if (
                            max(
                                evaluator.signals[
                                    index - evaluator.signal_valid_for : index
                                ]
                            )
                            == 1
                        ):
                            signals.append(1)
                        else:
                            signals.append(0)
                    except Exception:
                        signals.append(0)
            evaluator.signals = signals

    if evaluator.plot:
        await store_evaluator_plots(
            maker, evaluator.values, evaluator.signals, evaluator.second_values
        )
        _value_key = (
            maker.strategies[maker.current_strategy_id]
            .evaluators[maker.current_evaluator_id]
            .config_path_short
            + "lv"
            if maker.live_recording_mode
            else maker.strategies[maker.current_strategy_id]
            .evaluators[maker.current_evaluator_id]
            .config_path_short
            + "v"
        )
        await _plotting.plot(
            maker.ctx,
            evaluator.title,
            cache_value=_value_key,
            chart=evaluator.chart_location,
            color="green",
            mode="markers",
            line_shape=None,
        )
        if evaluator.second_values:
            await _plotting.plot(
                maker.ctx,
                evaluator.second_title,
                cache_value=_value_key + "2",
                chart=evaluator.second_chart_location,
                color="green",
                mode="markers",
                line_shape=None,
            )

    if maker.ctx.exchange_manager.is_backtesting:
        return {"v": evaluator.signals}
    try:
        current_signal = evaluator.signals[-1]
    except (KeyError, IndexError, TypeError):
        current_signal = evaluator.signals
    return {"v": current_signal}


async def allow_enable_plot(maker, evaluator, text="Plot Evaluator"):
    evaluator.plot = (
        await user_inputs2.user_input2(
            maker,
            evaluator,
            text,
            "boolean",
            True,
            show_in_summary=False,
            show_in_optimizer=False,
        )
        if maker.get_current_strategy().enable_plot
        else False
    )


def cut_data_to_same_len(data_set: tuple or list, get_list=False):
    # data tuple in and out
    min_len = None
    cutted_data: list = []

    for data in data_set:
        _len = len(data)
        if not min_len or _len < min_len:
            min_len = _len
    for data in data_set:
        cutted_data.append(data[len(data) - min_len :])
    if get_list or isinstance(data, list):
        return cutted_data
    return tuple(cutted_data)


async def plot_conditional(
    maker, indicator, cache_key, title, chart_location, bool_list, values
):
    if indicator.plot:
        if maker.ctx.exchange_manager.is_backtesting or (
            not maker.ctx.exchange_manager.is_backtesting
            and not maker.live_recording_mode
        ):
            data_len = min([len(bool_list), len(values)])
            t = await public_exchange_data.get_candles_(maker, "time")
            times_to_store = []
            values_to_store = []
            for index in range(1, data_len):
                if bool_list[-index]:
                    times_to_store.append(t[-index])
                    values_to_store.append(values[-index])
            await maker.ctx.set_cached_values(
                values=values_to_store,
                value_key=indicator.config_path_short + cache_key,
                cache_keys=times_to_store,
            )
        else:
            if bool_list[-1]:
                await maker.ctx.set_cached_value(
                    value=list(values)[-1],
                    value_key=indicator.config_path_short + cache_key,
                )
        await _plotting.plot(
            maker.ctx,
            title,
            cache_value=indicator.config_path_short + cache_key,
            chart=chart_location,
            mode="markers",
            line_shape=None,
        )
