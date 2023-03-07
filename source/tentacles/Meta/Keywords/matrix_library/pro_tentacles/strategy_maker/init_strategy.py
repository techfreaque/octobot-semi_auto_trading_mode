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

import octobot_trading.modes.script_keywords.basic_keywords as basic_keywords
import octobot_trading.modes.script_keywords.context_management as context_management
import tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix__enums
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.activate_managed_order as activate_managed_order
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.settings.sl_settings as sl_settings
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_keywords.orders.managed_order_pro.stop_losses.stop_loss_handling as stop_loss_handling
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.evaluators.evaluators_handling as evaluators_handling
import tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities


class StrategyData:
    enable_plot: bool = None
    live_recording_mode: bool = None

    def __init__(self, maker):
        self.supported_evaluators = maker.supported_evaluators
        self.signals = {}
        self.strategy_id = maker.current_strategy_id
        self.input_path = f"evaluator/Strategy_{maker.current_strategy_id + 1}_Settings"
        self.input_name = f"strategy_{maker.current_strategy_id + 1}_settings"
        self.config_path_short = f"s{self.strategy_id + 1}"
        self.trading_side = ""
        self.trading_side_key = ""
        self.nr_of_indicators = 0
        self.evaluators = {}
        self.strategy_signal = 0
        self.managed_order_root_name = f"S{self.strategy_id + 1}_Order_Settings"
        self.managed_order_root_name_prefix = f"S{self.strategy_id + 1}"
        self.managed_order_root_path = (
            f"evaluator/S{self.strategy_id + 1}_Order_Settings"
        )
        self.order_settings = None
        self.enable_strategy: bool = False

    async def build_and_trade_strategy_live(self, maker, ctx, strategy_only=False):
        await self.init_strategy(maker, strategy_only)
        if not self.enable_strategy:
            return
        self.strategy_signal = 0
        has_signal = 1
        for evaluator_id in range(0, self.nr_of_indicators):
            await self.get_evaluator(maker, ctx, evaluator_id)
            if self.evaluators and evaluator_id in self.evaluators:
                has_signal = self.strategy_signal = (
                    self.signals[evaluator_id] if has_signal == 1 else 0
                )
        if not strategy_only:
            await self.set_managed_order_settings(ctx, maker)
            if self.strategy_signal == 1:
                await self.execute_managed_order(ctx, maker)
            await self.handle_trailing_stop(ctx, maker)
        return self.strategy_signal

    async def build_strategy_backtesting_cache(self, maker, ctx):
        m_time = utilities.start_measure_time()
        await self.init_strategy(maker)
        if not self.enable_strategy:
            return
        for evaluator_id in range(0, self.nr_of_indicators):
            await self.get_evaluator(maker, ctx, evaluator_id)

        await self.set_managed_order_settings(ctx, maker)
        utilities.end_measure_time(
            m_time,
            f" strategy maker - calculating evaluators for strategy {self.strategy_id}",
            min_duration=9,
        )

    async def trade_strategy_backtesting(self, ctx, maker):
        await self.execute_managed_order(ctx, maker)

    async def init_strategy(self, maker, strategy_only=False):
        await basic_keywords.user_input(
            maker.ctx,
            self.config_path_short,
            input_type="object",
            title=f"Strategy_{maker.current_strategy_id + 1}_Settings",
            def_val=None,
            path=self.input_path,
            editor_options={
                "grid_columns": 12,
            },
            other_schema_values={"display_as_tab": True},
        )
        self.enable_strategy = await basic_keywords.user_input(
            maker.ctx,
            f"Enable Strategy ({self.config_path_short})",
            input_type="boolean",
            def_val=True,
            parent_input_name=self.config_path_short,
        )
        if not self.enable_strategy:
            return

        self.nr_of_indicators = await basic_keywords.user_input(
            maker.ctx,
            f"Amount of Evaluators combined together ({self.config_path_short})",
            "int",
            def_val=2,
            min_val=1,
            parent_input_name=self.config_path_short,
        )
        if not strategy_only:
            self.trading_side = await basic_keywords.user_input(
                maker.ctx,
                f"Trading direction (s{self.strategy_id + 1})",
                "options",
                def_val="long",
                options=["long", "short"],
                parent_input_name=self.config_path_short,
            )
        self.enable_plot = maker.enable_plot
        self.live_recording_mode = maker.live_recording_mode
        if (
            maker.ctx.exchange_manager.is_backtesting
            and maker.backtest_plotting_mode
            == matrix__enums.BacktestPlottingModes.ENABLE_PLOTTING
        ) or (
            maker.backtest_plotting_mode
            == matrix__enums.BacktestPlottingModes.ENABLE_PLOTTING
            or maker.live_plotting_mode
            in (
                matrix__enums.LivePlottingModes.PLOT_RECORDING_MODE,
                matrix__enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY,
            )
        ):
            self.enable_plot = await basic_keywords.user_input(
                maker.ctx,
                f"enable_plots_strategy_{self.strategy_id + 1}",
                "boolean",
                title="Enable plots for this strategy",
                def_val=True,
                parent_input_name=self.config_path_short,
            )
            if not self.enable_plot:
                self.live_recording_mode = True
        self.trading_side_key = "l" if self.trading_side == "long" else "s"
        # self.input_path = f"{self.input_path}/Strategy"

    async def get_evaluator(
        self, maker, ctx: context_management.Context, evaluator_id: int
    ):
        sm_time = utilities.start_measure_time()
        evaluator = evaluators_handling.Evaluator_(
            maker, self.input_name, self.config_path_short, self.supported_evaluators
        )
        maker.current_evaluator_id = evaluator_id
        await evaluator.init_evaluator(maker, ctx, evaluator_id)
        if evaluator.enabled:
            self.evaluators[evaluator_id] = evaluator
            self.signals[evaluator_id] = await evaluator.evaluate_and_get_data(
                maker, ctx
            )
            maker.evaluators[evaluator.config_path] = evaluator
            utilities.end_measure_time(
                sm_time,
                f" strategy maker - calculating evaluator {evaluator_id + 1} "
                f"{evaluator.name} {evaluator.class_name}",
                min_duration=9,
            )

    async def execute_managed_order(self, ctx, maker):
        await activate_managed_order.managed_order(
            maker,
            trading_side=self.trading_side,
            orders_settings=self.order_settings,
        )

    async def set_managed_order_settings(self, ctx, maker):
        await basic_keywords.user_input(
            ctx,
            self.managed_order_root_name,
            "object",
            title=self.managed_order_root_name.replace("_", " "),
            def_val=None,
            editor_options={
                "grid_columns": 12,
            },
            other_schema_values={"display_as_tab": True}
            # path=self.managed_order_root_path,
        )
        self.order_settings = await activate_managed_order.activate_managed_orders(
            maker,
            parent_input_name=self.managed_order_root_name,
            name_prefix=f"s{self.strategy_id + 1}",
            order_tag_prefix=f"Strategy {self.strategy_id+1}",
        )

    async def handle_trailing_stop(self, ctx, maker):
        for order_group_settings in self.order_settings.order_groups.values():
            if (
                order_group_settings.stop_loss.sl_trail_type
                != sl_settings.ManagedOrderSettingsSLTrailTypes.DONT_TRAIL_DESCRIPTION
            ):
                try:
                    await stop_loss_handling.trail_stop_losses(
                        maker,
                        order_group_settings=order_group_settings,
                        order_settings=self.order_settings,
                    )
                except Exception as error:
                    raise RuntimeError(
                        "Managed Order trailing Stop: There is probably an "
                        "issue in your Managed Order "
                        "configuration. Check the settings: " + str(error)
                    ) from error
