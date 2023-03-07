import enum

TAKE_PROFIT = "tp"
ENTRY = "e"
STOP_LOSS = "sl"

class PingPongOrderToOrderGroupIdConstants:
    GROUP_KEY = "group_key"
    ORDER_GROUP_ID = "order_group_id"
    GRID_ID = "grid_id"
    ENTRY_ORDER = "entry_order"


class PingPongConstants:
    FIRST_ORDER_CHAIN_ID = 0
    LAST_ORDER_CHAIN_ID = "last_order_chain_id"
    START_INFO_DATA: dict = {
        LAST_ORDER_CHAIN_ID: FIRST_ORDER_CHAIN_ID,
    }
    PING_PONG_INFO_STORAGE = "ping_pong_info_storage"
    PING_PONG_STORAGE = "ping_pong_storage"

    ENTRIES = "entries"
    EXITS = "exits"


class PingPongSingleDataColumns:
    GRID_ID = "grid_id"
    CALCULATED_ENTRY = "calculated_entry"
    ENTRY_COUNTER = "entry_counter"
    ORIGINAL_ENTRY_ORDER = "original_entry_order"
    ALL_RECREATED_ENTRY_ORDERS = "all_recreated_entry_orders"
    LAST_ORDER = "last_order"
    IS_FIRST_ENTRY = "is_first_entry"
    PING_PONG_ACTIVE = "ping_pong_active"
    EXIT_ORDERS = "exit_orders"
    ENTRY_ORDER = "entry_orders"


class PingPongOrderColumns(enum.Enum):
    SIDE = "side"
    AMOUNT = "amount"
    ENTRY_PRICE = "entry_price"
    ENTRY_TAG = "entry_tag"
    TAKE_PROFIT_PRICE = "take_profit_price"
    STOP_LOSS_PRICE = "stop_loss_price"
    TAKE_PROFIT_TAG = "take_profit_tag"
    STOP_LOSS_TAG = "stop_loss_tag"