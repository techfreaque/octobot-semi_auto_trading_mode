import decimal
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.settings.tp_settings as tp_settings
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.take_profits.based_on_indicator as based_on_indicator
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.take_profits.based_on_risk_reward as based_on_risk_reward
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.take_profits.based_on_percent as based_on_percent
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.take_profits.based_on_static_price as based_on_static_price


def get_manged_order_take_profits(
    maker,
    take_profit_settings,
    entry_side: str,
    current_price: decimal.Decimal,
    entry_price: decimal.Decimal,
    stop_loss_price: decimal.Decimal,
    entry_fee: decimal.Decimal,
    market_fee: decimal.Decimal,
) -> None or decimal.Decimal:
    if (
        tp_settings.ManagedOrderSettingsTPTypes.NO_TP_DESCRIPTION
        != take_profit_settings.tp_type
    ):
        # take profit based on risk reward
        if (
            take_profit_settings.tp_type
            == tp_settings.ManagedOrderSettingsTPTypes.SINGLE_RISK_REWARD_DESCRIPTION
        ):

            return based_on_risk_reward.calculate_take_profit_based_on_risk_reward(
                maker=maker,
                take_profit_settings=take_profit_settings,
                entry_side=entry_side,
                current_price=current_price,
                entry_price=entry_price,
                stop_loss_price=stop_loss_price,
                entry_fee=entry_fee,
                market_fee=market_fee,
            )

        # # scaled take profit based on risk reward
        # elif (
        #     take_profit_settings.tp_type
        #     == tp_settings.ManagedOrderSettingsTPTypes.SCALED_RISK_REWARD_DESCRIPTION
        # ):

        #         take_profits.calculate_take_profit_scaled_based_on_risk_reward(
        #             take_profit_settings, entry_price
        #         )

        # take profit based on percent
        elif (
            take_profit_settings.tp_type
            == tp_settings.ManagedOrderSettingsTPTypes.SINGLE_PERCENT_DESCRIPTION
        ):

            return based_on_percent.calculate_take_profit_based_on_percent(
                maker=maker,
                take_profit_settings=take_profit_settings,
                entry_side=entry_side,
                current_price=current_price,
                entry_price=entry_price,
                stop_loss_price=stop_loss_price,
                entry_fee=entry_fee,
                market_fee=market_fee,
            )
        # take profit based on indicator
        elif (
            take_profit_settings.tp_type
            == tp_settings.ManagedOrderSettingsTPTypes.SINGLE_INDICATOR_DESCRIPTION
        ):

            return based_on_indicator.calculate_take_profit_based_on_indicator(
                maker=maker,
                take_profit_settings=take_profit_settings,
                entry_side=entry_side,
                current_price=current_price,
                entry_price=entry_price,
                stop_loss_price=stop_loss_price,
                entry_fee=entry_fee,
                market_fee=market_fee,
            )

        # # scaled take profit based on percent
        # elif (
        #     take_profit_settings.tp_type
        #     == tp_settings.ManagedOrderSettingsTPTypes.SCALED_PERCENT_DESCRIPTION
        # ):

        #         take_profits.calculate_take_profit_scaled_based_on_percent(
        #             take_profit_settings, entry_price
        #         )

        # single take profit based on static price
        elif (
            take_profit_settings.tp_type
            == tp_settings.ManagedOrderSettingsTPTypes.SINGLE_STATIC_DESCRIPTION
        ):

            return based_on_static_price.calculate_take_profit_based_on_static_price(
                maker=maker,
                take_profit_settings=take_profit_settings,
                entry_side=entry_side,
                current_price=current_price,
                entry_price=entry_price,
                stop_loss_price=stop_loss_price,
                entry_fee=entry_fee,
                market_fee=market_fee,
            )

    return None
