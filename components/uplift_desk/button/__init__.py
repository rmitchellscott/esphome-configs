from esphome.core import coroutine
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_RESTART,
    ENTITY_CATEGORY_CONFIG,
    ENTITY_CATEGORY_DIAGNOSTIC,
    ENTITY_CATEGORY_CONFIG,
    CONF_COMMAND,
)
from .. import uplift_desk_ns, UPLIFT_DESK_COMPONENT_SCHEMA, CONF_UPLIFT_DESK_ID
from .const import *

AUTO_LOAD = ["uplift_desk"]

UpliftDeskButton = uplift_desk_ns.class_("UpliftDeskButton", cg.Component)

TYPES = [
    CONF_STOP,
    CONF_SAVE_PRESET_1,
    CONF_SAVE_PRESET_2,
    CONF_SAVE_PRESET_3,
    CONF_SAVE_PRESET_4,
    CONF_PRESET_1,
    CONF_PRESET_2,
    CONF_PRESET_3,
    CONF_PRESET_4,
    CONF_SYNC,
    CONF_LIMIT_SET_MIN,
    CONF_LIMIT_SET_MAX,
    CONF_LIMIT_CLEAR,
]


def uplift_desk_button_schema(
    command,
    icon: str = button._UNDEF,
    entity_category: str = button._UNDEF,
    device_class: str = button._UNDEF,
):
    return button.button_schema(
        icon=icon, entity_category=entity_category, device_class=device_class
    ).extend(
        {
            cv.GenerateID(): cv.declare_id(UpliftDeskButton),
            cv.Optional(CONF_COMMAND, default=command): cv.hex_int,
        }
    )


CONFIG_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_STOP): uplift_desk_button_schema(COMMAND_STOP, icon=ICON_STOP),
        cv.Optional(CONF_SAVE_PRESET_1): uplift_desk_button_schema(
            COMMAND_SAVE_PRESET_1,
            icon=ICON_FLOPPY,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        cv.Optional(CONF_SAVE_PRESET_2): uplift_desk_button_schema(
            COMMAND_SAVE_PRESET_2,
            icon=ICON_FLOPPY,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        cv.Optional(CONF_SAVE_PRESET_3): uplift_desk_button_schema(
            COMMAND_SAVE_PRESET_3,
            icon=ICON_FLOPPY,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        cv.Optional(CONF_SAVE_PRESET_4): uplift_desk_button_schema(
            COMMAND_SAVE_PRESET_4,
            icon=ICON_FLOPPY,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        cv.Optional(CONF_PRESET_1): uplift_desk_button_schema(
            COMMAND_PRESET_1, icon=ICON_NUMERIC_1_BOX
        ),
        cv.Optional(CONF_PRESET_2): uplift_desk_button_schema(
            COMMAND_PRESET_2, icon=ICON_NUMERIC_2_BOX
        ),
        cv.Optional(CONF_PRESET_3): uplift_desk_button_schema(
            COMMAND_PRESET_3, icon=ICON_NUMERIC_3_BOX
        ),
        cv.Optional(CONF_PRESET_4): uplift_desk_button_schema(
            COMMAND_PRESET_4, icon=ICON_NUMERIC_4_BOX
        ),
        cv.Optional(CONF_SYNC): uplift_desk_button_schema(
            COMMAND_SYNC, icon=ICON_SYNC, entity_category=ENTITY_CATEGORY_DIAGNOSTIC
        ),
        cv.Optional(CONF_LIMIT_SET_MIN): uplift_desk_button_schema(
            COMMAND_LIMIT_SET_MIN,
            icon=ICON_FORMAT_VERTICAL_ALIGN_BOTTOM,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        cv.Optional(CONF_LIMIT_SET_MAX): uplift_desk_button_schema(
            COMMAND_LIMIT_SET_MAX,
            icon=ICON_FORMAT_VERTICAL_ALIGN_TOP,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
        cv.Optional(CONF_LIMIT_CLEAR): uplift_desk_button_schema(
            COMMAND_LIMIT_CLEAR,
            icon=ICON_CLOSE_BOX,
            entity_category=ENTITY_CATEGORY_CONFIG,
        ),
    }
).extend(UPLIFT_DESK_COMPONENT_SCHEMA)


@coroutine
async def setup_conf(globalConfig, key, hub):
    if key in globalConfig:
        config = globalConfig[key]
        var = cg.new_Pvariable(config[CONF_ID])
        await cg.register_component(var, config)
        await button.register_button(var, config)

        cg.add(var.set_uplift_desk(hub))
        cg.add(var.set_command(config[CONF_COMMAND]))


def to_code(config):
    hub = yield cg.get_variable(config[CONF_UPLIFT_DESK_ID])
    for key in TYPES:
        yield setup_conf(config, key, hub)
