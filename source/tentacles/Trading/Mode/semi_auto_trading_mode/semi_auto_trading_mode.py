from octobot_trading.api import symbol_data
import octobot_commons.enums as common_enums
from octobot_trading.modes.script_keywords import basic_keywords
import tentacles.Meta.Keywords.matrix_library.matrix_basic_keywords.enums as matrix_enums

from tentacles.Meta.Keywords.priv_scripting_library.orders.order_types.order_manager.managed_orders import (
    activate_managed_orders,
    managed_order,
)
from tentacles.Meta.Keywords.scripting_library.UI.inputs import select_time_frame
from tentacles.Meta.Keywords.scripting_library.UI.inputs.select_history import (
    set_candles_history_size,
)
from tentacles.Trading.Mode.semi_auto_trading_mode.semi_auto_trading_mode_settings import (
    SemiAutoTradingModeSettings,
)


class SemiAutoTradeCommands:
    EXECUTE = "execute"


class SemiAutoTradingModeMaking(SemiAutoTradingModeSettings):

    strategy_mode: str = matrix_enums.StrategyModes.SEMI_AUTOMATED_TRADING
    should_execute_semi_auto: bool = False
    pairs_to_execute: list = None
    action: str = None

    async def _pre_script_call(self, context, action: dict or str = None):
        await self.make_strategy(context, action)

    async def make_strategy(self, ctx, action):
        self.action = action
        self.ctx = ctx
        await self.make_auto_strategy()

    async def make_semi_auto_strategy(self):
        self.ctx.enable_trading = False
        all_pairs = symbol_data.get_config_symbols(
            self.ctx.exchange_manager.config, True
        )
        self.trigger_time_frames = await select_time_frame.set_trigger_time_frames(
            self.ctx
        )
        await set_candles_history_size(self.ctx, 200)
        self.pairs_to_execute = await basic_keywords.user_input(
            self.ctx,
            "pairs_to_trade",
            common_enums.UserInputTypes.MULTIPLE_OPTIONS,
            title="Pairs to execute trades on",
            def_val=all_pairs,
            options=all_pairs,
            show_in_summary=True,
            show_in_optimizer=False,
        )

        all_pairs_settings_name: str = "all_pairs_settings"
        await basic_keywords.user_input(
            self.ctx,
            all_pairs_settings_name,
            common_enums.UserInputTypes.OBJECT,
            title="Order settings for all pairs",
            def_val=all_pairs,
            options=all_pairs,
            show_in_summary=True,
            show_in_optimizer=False,
        )
        trading_side_for_all: str = await basic_keywords.user_input(
            self.ctx,
            "trading_side",
            common_enums.UserInputTypes.OPTIONS,
            title="Trading side",
            def_val="long",
            options=["long", "short"],
            show_in_summary=True,
            show_in_optimizer=False,
            parent_input_name=all_pairs_settings_name,
        )
        managend_orders_settings_for_all = await activate_managed_orders(
            self.ctx, parent_input_name=all_pairs_settings_name
        )
        trading_sides: dict = {}
        managend_orders_settings: dict = {}

        for pair in self.pairs_to_execute:
            pair_settings_name: str = f"{pair} settings"
            await basic_keywords.user_input(
                self.ctx,
                pair_settings_name,
                common_enums.UserInputTypes.OBJECT,
                title=f"{pair} settings",
                def_val=None,
                show_in_summary=True,
                show_in_optimizer=False,
            )
            if await basic_keywords.user_input(
                self.ctx,
                f"{pair}_custom_settings_enabled",
                common_enums.UserInputTypes.BOOLEAN,
                title=f"Enable custom {pair} order settings",
                def_val=False,
                show_in_summary=True,
                show_in_optimizer=False,
                parent_input_name=pair_settings_name,
            ):
                trading_sides[pair] = await basic_keywords.user_input(
                    self.ctx,
                    f"{pair}_custom_trading_side",
                    common_enums.UserInputTypes.OPTIONS,
                    title=f"Trading side for {pair}",
                    def_val="long",
                    options=["long", "short"],
                    show_in_summary=True,
                    show_in_optimizer=False,
                    parent_input_name=pair_settings_name,
                )
                managend_orders_settings[pair] = await activate_managed_orders(
                    self.ctx, parent_input_name=pair_settings_name
                )
            else:
                managend_orders_settings[pair] = managend_orders_settings_for_all
                trading_sides[pair] = trading_side_for_all

            if (
                self.action
                and self.action == SemiAutoTradeCommands.EXECUTE
                and self.strategy_mode
                == matrix_enums.StrategyModes.SEMI_AUTOMATED_TRADING
                and self.ctx.symbol == pair
                and self.ctx.time_frame in self.trigger_time_frames
            ):
                self.ctx.enable_trading = True

                await managed_order(
                    self.ctx,
                    trading_side=trading_sides[pair],
                    orders_settings=managend_orders_settings[pair],
                )
