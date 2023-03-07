class ManagedOrderSettingsEntryTypes:
    SINGLE_MARKET_IN = "market_in"
    SINGLE_LIMIT_IN = "limit_in"
    SINGLE_TRY_LIMIT_IN = "try_limit_in"
    SCALED_OVER_TIME = "time_grid_orders"
    SCALED_DYNAMIC = "scaled_entry"
    SCALED_STATIC = "grid_entry"

    SINGLE_MARKET_IN_DESCRIPTION = "Single market in"
    SINGLE_LIMIT_IN_DESCRIPTION = "Single limit in"
    SINGLE_TRY_LIMIT_IN_DESCRIPTION = "Single try limit in"
    SCALED_OVER_TIME_DESCRIPTION = "Scale entry orders over time"
    SCALED_DYNAMIC_DESCRIPTION = "Scale limit orders over a dynamic price range"
    SCALED_STATIC_DESCRIPTION = "Scale limit orders over a static price range"

    KEY_TO_DESCRIPTIONS = {
        SINGLE_MARKET_IN: SINGLE_MARKET_IN_DESCRIPTION,
        SINGLE_LIMIT_IN: SINGLE_LIMIT_IN_DESCRIPTION,
        SINGLE_TRY_LIMIT_IN: SINGLE_TRY_LIMIT_IN_DESCRIPTION,
        SCALED_OVER_TIME: SCALED_OVER_TIME_DESCRIPTION,
        SCALED_DYNAMIC_DESCRIPTION: SCALED_DYNAMIC_DESCRIPTION,
        SCALED_STATIC: SCALED_STATIC_DESCRIPTION,
    }
    DESCRIPTIONS = [
        SINGLE_MARKET_IN_DESCRIPTION,
        SINGLE_LIMIT_IN_DESCRIPTION,
        # SINGLE_TRY_LIMIT_IN_DESCRIPTION,
        # SCALED_OVER_TIME_DESCRIPTION,
        SCALED_DYNAMIC_DESCRIPTION,
        SCALED_STATIC_DESCRIPTION,
    ]
