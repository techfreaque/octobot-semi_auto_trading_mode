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

import decimal
import octobot_trading.enums as trading_enums
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.stop_losses.stop_loss_handling as stop_loss_handling
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.standalone_data_source.standalone_data_sources as standalone_data_sources


def get_stop_loss_based_on_indicator(
    maker,
    stop_loss_settings,
    trading_side: str,
    entry_price: decimal.Decimal,
):

    sl_indicator_value = decimal.Decimal(
        str(
            standalone_data_sources.get_standalone_data_source(
                stop_loss_settings.sl_indicator_id, maker
            )
        )
    )
    if trading_side in (
        trading_enums.PositionSide.LONG.value,
        trading_enums.TradeOrderSide.BUY.value,
    ):
        sl_in_p, sl_price = stop_loss_handling.trim_sl_long_price(
            sl_indicator_value,
            entry_price,
            decimal.Decimal(str(stop_loss_settings.sl_max_p)),
            decimal.Decimal(str(stop_loss_settings.sl_min_p)),
        )

    elif trading_side in (
        trading_enums.PositionSide.SHORT.value,
        trading_enums.TradeOrderSide.SELL.value,
    ):
        sl_in_p, sl_price = stop_loss_handling.trim_sl_short_price(
            sl_indicator_value,
            entry_price,
            decimal.Decimal(str(stop_loss_settings.sl_max_p)),
            decimal.Decimal(str(stop_loss_settings.sl_min_p)),
        )
    else:
        raise RuntimeError('Side needs to be "long" or "short" for your managed order')
    return sl_in_p, sl_price
