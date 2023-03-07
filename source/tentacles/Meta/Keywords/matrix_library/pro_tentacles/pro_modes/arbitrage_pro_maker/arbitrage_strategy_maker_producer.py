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
import typing

import octobot_trading.modes.script_keywords.context_management as context_management
import octobot_trading.modes as trading_modes
import octobot_trading.enums as trading_enums
import octobot_trading.errors as errors
import octobot_commons.databases as databases
import octobot_commons.enums as commons_enums
import octobot_commons.errors as commons_errors
import octobot_commons.constants as commons_constants

import tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.data.public_exchange_data as public_exchange_data
import tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.tools.utilities as basic_utilities
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.pro_modes.indicator_only_mode as indicator_only_mode
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.trade_analysis.trade_analysis_activation as trade_analysis_activation
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.evaluators.supported_evaluators as supported_evaluators
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.strategy_maker.init_strategy as init_strategy
import tentacles.Meta.Keywords.matrix_library.basic_tentacles.matrix_basic_keywords.matrix_enums as matrix_enums
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.strategy_maker.strategy_building_base as strategy_building_base
import tentacles.Meta.Keywords.scripting_library.data.writing.plotting as plotting
import tentacles.Trading.Mode.arbitrage_pro_trading_mode.arbitrage_pro_settings.arbitrage_pro_settings as arbitrage_pro_settings


class ArbitrageProStrategyMakerProducer(
    trading_modes.AbstractTradingModeProducer,
    strategy_building_base.StrategyMakingBaseProducer,
):
    current_strategy_id = None
    supported_evaluators = supported_evaluators.get_supported_evaluators()
    enable_plot = True
    default_live_plotting_mode: str = (
        matrix_enums.LivePlottingModes.PLOT_RECORDING_MODE.value
    )
    default_backtest_plotting_mode: str = (
        matrix_enums.BacktestPlottingModes.DISABLE_PLOTTING.value
    )
    live_plotting_modes: list = [
        matrix_enums.LivePlottingModes.DISABLE_PLOTTING.value,
        matrix_enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY.value,
        matrix_enums.LivePlottingModes.PLOT_RECORDING_MODE.value,
    ]
    backtest_plotting_modes: list = [
        matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING.value,
        matrix_enums.BacktestPlottingModes.DISABLE_PLOTTING.value,
    ]

    backtest_plotting_mode = matrix_enums.BacktestPlottingModes.ENABLE_PLOTTING
    live_plotting_mode = matrix_enums.LivePlottingModes.REPLOT_VISIBLE_HISTORY
    last_calls_by_bot_id_and_time_frame: dict = {}

    def __init__(self, channel, config, trading_mode, exchange_manager):
        trading_modes.AbstractTradingModeProducer.__init__(
            self, channel, config, trading_mode, exchange_manager
        )
        strategy_building_base.StrategyMakingBaseProducer.__init__(
            self, channel, config, trading_mode, exchange_manager
        )
        self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR: dict = {}
        self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR: dict = {}
        # TODO
        self.debug_mode = True

        self.strategy_signals = {}
        self.strategy_name = ""
        # self.is_backtesting = None
        # self.trigger_time_frames = []
        self.nr_of_strategies = 2
        self.candles = {}
        self.strategies: typing.Dict[int, init_strategy.StrategyData] = {}
        self.evaluators = {}
        self.indicators = {}
        self.current_evaluator_id = None
        self.current_indicator_id = None
        self.live_plotting_mode = False
        self.live_recording_mode = False
        self.plot_signals = True
        # self.whitelist_mode = True
        self.input_path = None
        self.input_parent_backtesting = "backtesting_settings"
        self.input_parent_live = "live_settings"
        self.config_path_short = "m"
        self.strategy_cache = {}
        self.managed_order_indicator_cache = {}
        self.all_timestamps = None
        self.any_trading_timestamps = None
        self.ctx: context_management.Context = None
        self.backtesting_mode = ""
        self.trade_analysis_mode_settings = {}
        self.all_winrates = {}
        self.consumable_indicator_cache = {}
        self.standalone_indicators = {}
        self.enable_skip_runs = False
        self.skip_runs_balance_below = 0
        self.trade_analysis_activated = False
        # self.current_indicator_time_frame: strategy_builder_enums = None

    async def call_strategy_maker(self, exchange_name):
        if self.ctx.exchange_manager.is_backtesting:
            await self.call_strategy_maker_backtesting(exchange_name)
        else:
            await self.call_strategy_maker_live(exchange_name)

    async def call_strategy_maker_backtesting(self, exchange_name):
        await trade_analysis_activation.handle_trade_analysis_for_current_candle(
            self.ctx, parent_input=None  # self.plot_settings_name,
        )
        if self.exchange_name in self.trading_mode.arbitrage_settings.trend_exchanges:
            if self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR.get(
                exchange_name, {}
            ).get(self.ctx.symbol):
                if not self.consumable_indicator_cache:
                    await indicator_only_mode.run_indicator_only_mode(
                        self,
                    )
                pass
            else:
                s_time = basic_utilities.start_measure_time(
                    " strategy maker - building backtesting cache"
                )
                # TODO allow settings
                # await self.init_strategy_maker(is_backtesting=True)

                self.all_timestamps = await public_exchange_data.get_candles_(
                    self, "time"
                )
                if (
                    exchange_name
                    not in self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR
                ):
                    self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name] = {}
                if (
                    self.ctx.symbol
                    not in self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[
                        exchange_name
                    ]
                ):
                    self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name][
                        self.ctx.symbol
                    ] = {}
                for strategy_id in range(self.nr_of_strategies):
                    await self.build_strategy_backtesting_cache(strategy_id)

                (
                    self.any_trading_timestamps,
                    trades_count,
                ) = await self.merge_signals_in_backtesting()

                self.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name][
                    self.ctx.symbol
                ] = self.strategy_cache
                # TODO handle whitelist mode
                # self.handle_backtesting_timestamp_whitelist()
                # self.trading_mode.set_initialized_trading_pair_by_bot_id(
                #     self.ctx.symbol, self.ctx.time_frame, initialized=True
                # )
                basic_utilities.end_measure_time(
                    s_time,
                    f" strategy maker - building strategy for "
                    f"{self.ctx.time_frame} / {trades_count} candles allowed to trade",
                )
        else:
            await plotting.plot(
                self.ctx,
                title="trade signal",
                cache_value="arb_trd",
                mode="markers",
                line_shape=None,
            )

    async def call_strategy_maker_live(self, exchange_name):
        # TODO only execute when trend_exchange
        # user inputs not loading properly when skipped
        # if self.exchange_name in self.trading_mode.arbitrage_settings.trend_exchanges:

        # TODO allow settings
        # await self.init_strategy_maker(is_backtesting=True)

        for strategy_id in range(self.nr_of_strategies):
            self.current_strategy_id = strategy_id
            self.strategies[
                self.current_strategy_id
            ]: init_strategy.StrategyData = init_strategy.StrategyData(self)

            signal = bool(
                await self.strategies[
                    self.current_strategy_id
                ].build_and_trade_strategy_live(self, self.ctx, strategy_only=True)
            )
            if exchange_name not in self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR:
                self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name] = {}
            if (
                self.ctx.symbol
                not in self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name]
            ):
                self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name][
                    self.ctx.symbol
                ] = {}
            self.LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[exchange_name][self.ctx.symbol][
                strategy_id
            ] = signal

            if (
                self.exchange_name
                in self.trading_mode.arbitrage_settings.trend_exchanges
            ):
                self.logger.info(
                    f"Strategy {strategy_id} "
                    f"{'allowed to trade' if signal else 'not allowed to trade'} on"
                    f" {exchange_name} {self.ctx.symbol} {self.ctx.time_frame}"
                )
        await trade_analysis_activation.handle_trade_analysis_for_current_candle(
            self.ctx, parent_input=None  # self.plot_settings_name,
        )
        await indicator_only_mode.run_indicator_only_mode(self)

    async def get_strategy_signal(
        self,
        traded_exchange_name,
        trading_side: trading_enums.EvaluatorStates,
        symbol: str,
        mark_price: decimal.Decimal,
    ) -> bool:
        exchange_settings = self.trading_mode.arbitrage_settings.exchange_settings[
            traded_exchange_name
        ]
        if trading_side == trading_enums.EvaluatorStates.LONG:
            strategy_id = exchange_settings.long_strategy_id - 1
        elif trading_side == trading_enums.EvaluatorStates.SHORT:
            strategy_id = exchange_settings.short_strategy_id - 1
        if self.exchange_manager.is_backtesting:
            return await self.get_backtesting_strategy_signal(
                strategy_id, exchange_settings, symbol, mark_price
            )
        else:
            return self.get_live_strategy_signal(strategy_id, exchange_settings, symbol)

    async def get_backtesting_strategy_signal(
        self,
        strategy_id: int,
        exchange_settings,
        symbol: str,
        mark_price: decimal.Decimal,
    ) -> bool:
        timestamp = self.ctx.trigger_value[0]
        evaluation_mode_producer = get_evaluation_mode_producer(self, exchange_settings)
        signals_cache = (
            evaluation_mode_producer.BACKTESTING_STRATEGIES_BY_EXCHANGE_AND_PAIR[
                exchange_settings.evaluation_exchange
            ][symbol]
        )
        if signals_cache.get(timestamp, {}).get(strategy_id):
            await self.ctx.set_cached_values(
                value_key="arb_trd",
                values=[float(str(mark_price))],
                cache_keys=[timestamp],
            )
            return True
        return False

    def get_live_strategy_signal(
        self,
        strategy_id: int,
        exchange_settings: arbitrage_pro_settings.ArbitrageProExchangeSettings,
        symbol: str,
    ) -> bool:
        try:
            return get_evaluation_mode_producer(
                self, exchange_settings
            ).LIVE_STRATEGIES_BY_EXCHANGE_AND_PAIR[
                exchange_settings.evaluation_exchange
            ][
                symbol
            ][
                strategy_id
            ]
        except KeyError:
            return False

    async def candle_callback(
        self,
        exchange: str,
        exchange_id: str,
        cryptocurrency: str,
        symbol: str,
        time_frame: str,
        candle: dict,
        trigger_source=commons_enums.ActivationTopics.FULL_CANDLES.value,
    ):
        async with self.trading_mode_trigger():
            # add a full candle to time to get the real time
            trigger_time = (
                candle[commons_enums.PriceIndexes.IND_PRICE_TIME.value]
                + commons_enums.TimeFramesMinutes[commons_enums.TimeFrames(time_frame)]
                * commons_constants.MINUTE_TO_SECONDS
            )
            self.log_last_call_by_exchange_id(
                matrix_id=self.matrix_id,
                exchange=exchange,
                cryptocurrency=cryptocurrency,
                symbol=symbol,
                time_frame=time_frame,
                trigger_cache_timestamp=trigger_time,
                candle=candle,
            )
            await self.pre_strategy_maker_call(
                self.matrix_id,
                exchange=exchange,
                cryptocurrency=cryptocurrency,
                symbol=symbol,
                time_frame=time_frame,
                trigger_cache_timestamp=trigger_time,
                candle=candle,
            )

    async def pre_strategy_maker_call(
        self,
        matrix_id,
        exchange,
        cryptocurrency,
        symbol,
        time_frame,
        trigger_cache_timestamp,
        candle,
    ):
        self.ctx = context_management.get_full_context(
            trading_mode=self.trading_mode,
            matrix_id=matrix_id,
            cryptocurrency=cryptocurrency,
            symbol=symbol,
            time_frame=time_frame,
            trigger_source=commons_enums.ActivationTopics.FULL_CANDLES.value,
            trigger_cache_timestamp=trigger_cache_timestamp,
            candle=candle,
            kline=None,
            init_call=False,
        )

        self.ctx.matrix_id = matrix_id
        self.ctx.cryptocurrency = cryptocurrency
        self.ctx.symbol = symbol
        self.ctx.time_frame = time_frame
        initialized = True
        run_data_writer = databases.RunDatabasesProvider.instance().get_run_db(
            self.exchange_manager.bot_id
        )
        try:
            # if self.exchange_name in self.trading_mode.trend_exchanges:
            await self.call_strategy_maker(exchange)
        except errors.UnreachableExchange:
            raise
        except (
            commons_errors.MissingDataError,
            commons_errors.ExecutionAborted,
        ) as error:
            self.logger.debug(f"Strategy evaluation aborted: {error}")
            initialized = run_data_writer.are_data_initialized
        except Exception as error:
            self.logger.exception(error, True, f"Strategy evaluation failed: {error}")
        finally:
            if not self.exchange_manager.is_backtesting:
                if self.ctx.has_cache(self.ctx.symbol, self.ctx.time_frame):
                    await self.ctx.get_cache().flush()
                for symbol in self.exchange_manager.exchange_config.traded_symbol_pairs:
                    await databases.RunDatabasesProvider.instance().get_symbol_db(
                        self.exchange_manager.bot_id,
                        self.exchange_manager.exchange_name,
                        symbol,
                    ).flush()
            run_data_writer.set_initialized_flags(initialized)
            databases.RunDatabasesProvider.instance().get_symbol_db(
                self.exchange_manager.bot_id, self.exchange_name, symbol
            ).set_initialized_flags(initialized, (time_frame,))

    def log_last_call_by_exchange_id(
        self,
        matrix_id,
        exchange,
        cryptocurrency,
        symbol,
        time_frame,
        trigger_cache_timestamp,
        candle,
    ):
        if self.exchange_manager.bot_id not in self.last_calls_by_bot_id_and_time_frame:
            self.last_calls_by_bot_id_and_time_frame[self.exchange_manager.bot_id] = {}
        if (
            time_frame
            not in self.last_calls_by_bot_id_and_time_frame[
                self.exchange_manager.bot_id
            ]
        ):
            self.last_calls_by_bot_id_and_time_frame[self.exchange_manager.bot_id][
                time_frame
            ] = {}

        self.last_calls_by_bot_id_and_time_frame[self.exchange_manager.bot_id][
            time_frame
        ][symbol] = (
            matrix_id,
            exchange,
            cryptocurrency,
            symbol,
            time_frame,
            trigger_cache_timestamp,
            candle,
        )

    async def post_trigger(self):
        if not self.exchange_manager.is_backtesting:
            # update db after each run only in live mode
            for database in self.all_databases().values():
                if database:
                    try:
                        await database.flush()
                    except Exception as err:
                        self.logger.exception(
                            err, True, f"Error when flushing database: {err}"
                        )


def get_evaluation_mode_producer(
    producer: ArbitrageProStrategyMakerProducer, exchange_settings
) -> ArbitrageProStrategyMakerProducer:
    return (
        producer.exchange_managers_by_exchange_name[
            exchange_settings.evaluation_exchange
        ]
        .trading_modes[0]
        .producers[0]
    )
