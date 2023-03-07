import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.settings.all_settings as all_settings
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.managed_orders as managed_orders


async def activate_managed_orders(
    maker,
    # user_input_path: str = "evaluator/Managed_Order_Settings",
    parent_input_name: str = None,
    order_tag_prefix: str = "Managed order",
    name_prefix: str = None,
) -> all_settings.ManagedOrdersSettings:

    try:
        orders_settings = all_settings.ManagedOrdersSettings()
        await orders_settings.initialize(
            maker,
            parent_user_input_name=parent_input_name,
            order_tag_prefix=order_tag_prefix,
            unique_name_prefix=name_prefix,
        )
        return orders_settings
    except Exception as error:
        raise RuntimeError(
            "Managed Order: There is an issue in your Managed Order "
            "configuration. Check the settings: " + str(error)
        ) from error


async def managed_order(
    maker,
    trading_side: str,
    orders_settings: all_settings.ManagedOrdersSettings,
    order_preview_mode: bool = False,
) -> managed_orders.ManagedOrder:
    """
    :param maker:
    :param trading_side:
        can be "long" or short
    :param orders_settings:
        pass custom settings or use activate_managed_orders(ctx)

    :return:
    """
    _managed_order = managed_orders.ManagedOrder()
    return await _managed_order.initialize_and_trade(
        maker=maker,
        trading_side=trading_side,
        orders_settings=orders_settings,
        order_preview_mode=order_preview_mode,
    )


async def managed_order_preview(
    maker,
    trading_side: str,
    orders_settings: all_settings.ManagedOrdersSettings,
) -> managed_orders.ManagedOrder or None:
    if not maker.exchange_manager.is_backtesting:
        return await managed_order(
            maker,
            trading_side=trading_side,
            orders_settings=orders_settings,
            order_preview_mode=True,
        )
