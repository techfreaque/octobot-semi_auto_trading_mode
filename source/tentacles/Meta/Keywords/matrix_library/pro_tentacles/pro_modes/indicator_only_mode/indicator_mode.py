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
import tentacles.Meta.Keywords.matrix_library.pro_tentacles.standalone_data_source.standalone_data_sources as standalone_data_sources


INDICATOR_ONLY_MODE_SETTINGS_NAME = "indicator_only_mode_settings"


async def run_indicator_only_mode(maker, init_only=False):
    activate_indicator_only_mode = await basic_keywords.user_input(
        maker.ctx,
        "amount_of_indicators",
        input_type="boolean",
        title="Activate plot only indicators",
        def_val=False,
    )
    if activate_indicator_only_mode:
        await basic_keywords.user_input(
            maker.ctx,
            INDICATOR_ONLY_MODE_SETTINGS_NAME,
            input_type="object",
            title="Plot only indicators",
            def_val=None,
            editor_options={
                "grid_columns": 12,
            },
            other_schema_values={"display_as_tab": True},
        )
        amount_of_indicators = await basic_keywords.user_input(
            maker.ctx,
            "amount_of_indicators",
            input_type="int",
            title="Amount of indicators",
            def_val=0,
            min_val=0,
            parent_input_name=INDICATOR_ONLY_MODE_SETTINGS_NAME,
            editor_options={
                "grid_columns": 12,
            },
        )
        for indicator_id in range(amount_of_indicators):
            this_indicator_id = indicator_id + 700 + 1
            this_indicator_settings_name = f"indicator_settings_{this_indicator_id}"
            await basic_keywords.user_input(
                maker.ctx,
                this_indicator_settings_name,
                input_type="object",
                title=f"Indicator_settings_{indicator_id+1}",
                def_val=None,
                editor_options={
                    "grid_columns": 12,
                },
                parent_input_name=INDICATOR_ONLY_MODE_SETTINGS_NAME,
            )
            await standalone_data_sources.activate_standalone_data_source(
                f"Indicator {indicator_id+1}",
                parent_input_name=this_indicator_settings_name,
                indicator_id=this_indicator_id,
                maker=maker,
            )
            if not init_only:
                standalone_data_sources.get_standalone_data_source(
                    this_indicator_id, maker
                )
