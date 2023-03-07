import decimal as decimal
import typing
from tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.settings import (
    sl_settings,
)

from tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.settings.sl_settings import (
    ManagedOrderSettingsSLTypes,
)
import tentacles.Meta.Keywords.scripting_library.data.reading.exchange_public_data as exchange_public_data

import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.stop_losses.stop_loss_types as stop_loss_types


async def get_manged_order_stop_loss(
    maker,
    stop_loss_settings,
    trading_side,
    entry_price: decimal.Decimal,
    current_price: decimal.Decimal,
    get_from_current_price: bool = False,
) -> typing.Tuple[float, float]:
    sl_price: float = None
    sl_in_p: float = None
    current_price = current_price or float(
        await exchange_public_data.current_live_price(maker.ctx)
    )
    entry_price = entry_price or current_price
    if trading_side == "buy":
        entry_price = entry_price if entry_price < current_price else current_price
    else:
        entry_price = entry_price if entry_price > current_price else current_price
    if (
        stop_loss_settings.sl_type
        != sl_settings.ManagedOrderSettingsSLTypes.NO_SL_DESCRIPTION
    ):
        # SL based on low/high
        if (
            stop_loss_settings.sl_type
            == sl_settings.ManagedOrderSettingsSLTypes.AT_LOW_HIGH_DESCRIPTION
        ):
            sl_in_p, sl_price = await stop_loss_types.get_stop_loss_based_on_low_high(
                maker=maker,
                stop_loss_settings=stop_loss_settings,
                trading_side=trading_side,
                entry_price=current_price if get_from_current_price else entry_price,
            )
        # SL based on percent
        elif (
            stop_loss_settings.sl_type
            == ManagedOrderSettingsSLTypes.BASED_ON_PERCENT_DESCRIPTION
        ):
            sl_in_p, sl_price = stop_loss_types.get_stop_loss_based_on_percent(
                maker=maker,
                stop_loss_settings=stop_loss_settings,
                trading_side=trading_side,
                entry_price=current_price if get_from_current_price else entry_price,
            )
        # SL based on indicator
        elif (
            stop_loss_settings.sl_type
            == ManagedOrderSettingsSLTypes.BASED_ON_INDICATOR_DESCRIPTION
        ):
            sl_in_p, sl_price = stop_loss_types.get_stop_loss_based_on_indicator(
                maker=maker,
                stop_loss_settings=stop_loss_settings,
                trading_side=trading_side,
                entry_price=current_price if get_from_current_price else entry_price,
            )
        # SL based on static price
        elif (
            stop_loss_settings.sl_type
            == ManagedOrderSettingsSLTypes.BASED_ON_STATIC_PRICE_DESCRIPTION
        ):
            sl_in_p, sl_price = stop_loss_types.get_stop_loss_based_on_static_price(
                maker=maker,
                stop_loss_settings=stop_loss_settings,
                trading_side=trading_side,
                entry_price=current_price if get_from_current_price else entry_price,
            )

        # SL based on ATR
        elif (
            stop_loss_settings.sl_type
            == ManagedOrderSettingsSLTypes.BASED_ON_ATR_DESCRIPTION
        ):
            sl_in_p, sl_price = await stop_loss_types.get_stop_loss_based_on_atr(
                maker=maker,
                stop_loss_settings=stop_loss_settings,
                trading_side=trading_side,
                entry_price=current_price if get_from_current_price else entry_price,
            )
        return (
            exchange_public_data.get_digits_adapted_price(maker.ctx, sl_price),
            sl_in_p,
        )
        # no SL
    return None, None
