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

import octobot_trading.modes.script_keywords.basic_keywords.account_balance as account_balance
import octobot_trading.modes.script_keywords.basic_keywords.user_inputs as user_inputs
import tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.data.exchange_private_data as exchange_private_data
import tentacles.Meta.Keywords.scripting_library.data.writing.plotting as plotting


async def plot_orders(ctx, parent_input):
    # plot orders
    activate_plot_orders = await user_inputs.user_input(
        ctx,
        "plot orders",
        "boolean",
        def_val=True,
        parent_input_name=parent_input,
        show_in_summary=False,
        show_in_optimizer=False,
    )
    if activate_plot_orders:
        _open_orders = (
            ctx.exchange_manager.exchange_personal_data.orders_manager.get_open_orders(
                symbol=ctx.symbol
            )
        )
        tp_list = []
        sl_list = []
        limit_list = []
        entry_list = []
        for order in _open_orders:
            if order.exchange_order_type.name == "STOP_LOSS":
                sl_list.append(float(order.origin_price))
                # todo change based on trades
                entry_list.append(float(order.created_last_price))
            elif order.reduce_only is True:
                tp_list.append(float(order.origin_price))
            elif order.exchange_order_type.name == "LIMIT":
                limit_list.append(float(order.origin_price))
            elif order.exchange_order_type.name == "MARKET":
                entry_list.append(float(order.origin_price))
        if ctx.exchange_manager.is_backtesting:
            if tp_list:
                await ctx.set_cached_value(value=tp_list, value_key="tp")
            if sl_list:
                await ctx.set_cached_value(value=sl_list, value_key="sl")
            if entry_list:
                await ctx.set_cached_value(value=entry_list, value_key="entry")
            if limit_list:
                await ctx.set_cached_value(value=entry_list, value_key="lmt")
            try:
                await plotting.plot(
                    ctx,
                    "stop losses",
                    cache_value="sl",
                    mode="markers",
                    chart="main-chart",
                    color="yellow",
                    shift_to_open_candle_time=False,
                )
                await plotting.plot(
                    ctx,
                    "take profits",
                    cache_value="tp",
                    mode="markers",
                    chart="main-chart",
                    color="magenta",
                    shift_to_open_candle_time=False,
                )
                await plotting.plot(
                    ctx,
                    "entries",
                    cache_value="entry",
                    mode="markers",
                    chart="main-chart",
                    color="blue",
                    shift_to_open_candle_time=False,
                )
                await plotting.plot(
                    ctx,
                    "limit orders",
                    cache_value="lmt",
                    mode="markers",
                    chart="main-chart",
                    color="magenta",
                    shift_to_open_candle_time=False,
                )
            except RuntimeError:
                pass  # no cache
        else:
            if tp_list:
                await ctx.set_cached_value(value=tp_list, value_key="l-tp")
            if sl_list:
                await ctx.set_cached_value(value=sl_list, value_key="l-sl")
            if entry_list:
                await ctx.set_cached_value(value=entry_list, value_key="l-entry")
            if limit_list:
                await ctx.set_cached_value(value=limit_list, value_key="l-lmt")
            try:
                await plotting.plot(
                    ctx,
                    "stop losses",
                    cache_value="l-sl",
                    mode="markers",
                    chart="main-chart",
                    color="yellow",
                    shift_to_open_candle_time=False,
                )
                await plotting.plot(
                    ctx,
                    "take profits",
                    cache_value="l-tp",
                    mode="markers",
                    chart="main-chart",
                    color="magenta",
                    shift_to_open_candle_time=False,
                )
                # todo live entries are wrong (same as sl)
                # await plotting.plot(ctx, "entries", cache_value="l-entry", mode="markers", chart="main-chart",
                #                     color="blue", shift_to_open_candle_time=False)
                await plotting.plot(
                    ctx,
                    "limit orders",
                    cache_value="l-lmt",
                    mode="markers",
                    chart="main-chart",
                    color="magenta",
                    shift_to_open_candle_time=False,
                )
            except RuntimeError:
                pass  # no cache


async def plot_current_position(ctx, parent_input):
    enable_plot_position = await user_inputs.user_input(
        ctx,
        "plot open position",
        "boolean",
        def_val=True,
        parent_input_name=parent_input,
        show_in_summary=False,
        show_in_optimizer=False,
    )
    if enable_plot_position:
        try:
            current_pos = exchange_private_data.get_position_size(ctx)
        except AttributeError:
            print("plot position error")
            current_pos = 0
        if ctx.exchange_manager.is_backtesting:
            try:
                await ctx.set_cached_value(value=float(current_pos), value_key="op")
            except:
                pass
            await plotting.plot(
                ctx,
                "current position",
                cache_value="op",
                chart="sub-chart",
                color="blue",
                shift_to_open_candle_time=False,
                mode="markers",
                own_yaxis=True,
            )
        else:
            try:
                await ctx.set_cached_value(value=float(current_pos), value_key="l-op")
            except:
                pass

            await plotting.plot(
                ctx,
                "current position",
                cache_value="l-op",
                chart="sub-chart",
                color="blue",
                shift_to_open_candle_time=False,
                mode="markers",
                own_yaxis=True,
            )


async def plot_average_entry(ctx, parent_input):
    enable_plot_entry = await user_inputs.user_input(
        ctx,
        "plot average entry",
        "boolean",
        def_val=True,
        parent_input_name=parent_input,
        show_in_summary=False,
        show_in_optimizer=False,
    )
    if enable_plot_entry and ctx.exchange_manager.is_future:
        try:
            current_entry = (
                ctx.exchange_manager.exchange_personal_data.positions_manager.positions[
                    ctx.symbol
                ].entry_price
            )
        except (AttributeError, KeyError):
            return
        key = "b-" if ctx.exchange_manager.is_backtesting else "l-"
        if current_entry:
            await ctx.set_cached_value(value=float(current_entry), value_key=key + "ae")
        await plotting.plot(
            ctx,
            "current average entry",
            cache_value=key + "ae",
            chart="main-chart",
            color="blue",
            shift_to_open_candle_time=False,
            mode="markers",
        )


async def plot_balances(ctx, parent_input):
    enable_plot_balances = await user_inputs.user_input(
        ctx,
        "plot balances",
        "boolean",
        def_val=True,
        show_in_summary=False,
        show_in_optimizer=False,
        parent_input_name=parent_input,
    )
    if enable_plot_balances:
        key = "b-" if ctx.exchange_manager.is_backtesting else "l-"
        current_total_balance = (
            ctx.exchange_manager.exchange_personal_data.portfolio_manager.portfolio_value_holder.portfolio_current_value
        )

        await ctx.set_cached_value(
            value=float(current_total_balance), value_key=key + "cb"
        )
        await plotting.plot(
            ctx,
            "current balance",
            cache_value=key + "cb",
            chart="sub-chart",
            color="blue",
            shift_to_open_candle_time=False,
            mode="markers",
        )
        current_available_balance = await account_balance.available_account_balance(ctx)
        await ctx.set_cached_value(
            value=float(current_available_balance), value_key=key + "cab"
        )
        await plotting.plot(
            ctx,
            "current available balance",
            cache_value=key + "cab",
            chart="sub-chart",
            color="blue",
            shift_to_open_candle_time=False,
            mode="markers",
        )
