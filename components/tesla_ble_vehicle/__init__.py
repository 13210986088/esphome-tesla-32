import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import ble_client, binary_sensor, button, switch, number, sensor, text_sensor, lock, cover, climate
from esphome.const import (
    CONF_ACCURACY_DECIMALS,
    CONF_DEVICE_CLASS,
    CONF_DISABLED_BY_DEFAULT,
    CONF_ENTITY_CATEGORY,
    CONF_FORCE_UPDATE,
    CONF_ICON,
    CONF_ID,
    CONF_INTERNAL,
    CONF_MODE,
    CONF_NAME,
    CONF_RESTORE_MODE,
    CONF_UNIT_OF_MEASUREMENT,
)
from esphome import automation


CODEOWNERS = ["@yoziru"]
DEPENDENCIES = ["ble_client"]
AUTO_LOAD = ["binary_sensor", "button", "switch", "number", "sensor", "text_sensor", "lock", "cover", "climate"]

tesla_ble_vehicle_ns = cg.esphome_ns.namespace("tesla_ble_vehicle")
TeslaBLEVehicle = tesla_ble_vehicle_ns.class_(
    "TeslaBLEVehicle", cg.PollingComponent, ble_client.BLEClientNode
)

# Custom button classes
TeslaWakeButton = tesla_ble_vehicle_ns.class_("TeslaWakeButton", button.Button)
TeslaPairButton = tesla_ble_vehicle_ns.class_("TeslaPairButton", button.Button)
TeslaRegenerateKeyButton = tesla_ble_vehicle_ns.class_("TeslaRegenerateKeyButton", button.Button)
TeslaForceUpdateButton = tesla_ble_vehicle_ns.class_("TeslaForceUpdateButton", button.Button)
TeslaFlashLightsButton = tesla_ble_vehicle_ns.class_("TeslaFlashLightsButton", button.Button)
TeslaHonkHornButton = tesla_ble_vehicle_ns.class_("TeslaHonkHornButton", button.Button)
TeslaUnlatchDriverDoorButton = tesla_ble_vehicle_ns.class_("TeslaUnlatchDriverDoorButton", button.Button)
TeslaStartDrivingButton = tesla_ble_vehicle_ns.class_("TeslaStartDrivingButton", button.Button)

# Custom switch classes
TeslaChargingSwitch = tesla_ble_vehicle_ns.class_("TeslaChargingSwitch", switch.Switch)
TeslaSteeringWheelHeatSwitch = tesla_ble_vehicle_ns.class_("TeslaSteeringWheelHeatSwitch", switch.Switch)
TeslaSentryModeSwitch = tesla_ble_vehicle_ns.class_("TeslaSentryModeSwitch", switch.Switch)

# Custom lock classes
TeslaDoorsLock = tesla_ble_vehicle_ns.class_("TeslaDoorsLock", lock.Lock)
TeslaChargePortLatchLock = tesla_ble_vehicle_ns.class_("TeslaChargePortLatchLock", lock.Lock)

# Custom cover classes
TeslaTrunkCover = tesla_ble_vehicle_ns.class_("TeslaTrunkCover", cover.Cover)
TeslaFrunkCover = tesla_ble_vehicle_ns.class_("TeslaFrunkCover", cover.Cover)
TeslaWindowsCover = tesla_ble_vehicle_ns.class_("TeslaWindowsCover", cover.Cover)
TeslaChargePortDoorCover = tesla_ble_vehicle_ns.class_("TeslaChargePortDoorCover", cover.Cover)

# Custom climate class
TeslaClimate = tesla_ble_vehicle_ns.class_("TeslaClimate", climate.Climate)

# Custom number classes
TeslaChargingAmpsNumber = tesla_ble_vehicle_ns.class_("TeslaChargingAmpsNumber", number.Number)
TeslaChargingLimitNumber = tesla_ble_vehicle_ns.class_("TeslaChargingLimitNumber", number.Number)

# Actions
WakeAction = tesla_ble_vehicle_ns.class_("WakeAction", automation.Action)
PairAction = tesla_ble_vehicle_ns.class_("PairAction", automation.Action)
RegenerateKeyAction = tesla_ble_vehicle_ns.class_("RegenerateKeyAction", automation.Action)
ForceUpdateAction = tesla_ble_vehicle_ns.class_("ForceUpdateAction", automation.Action)
SetChargingAction = tesla_ble_vehicle_ns.class_("SetChargingAction", automation.Action)
SetChargingAmpsAction = tesla_ble_vehicle_ns.class_("SetChargingAmpsAction", automation.Action)
SetChargingLimitAction = tesla_ble_vehicle_ns.class_("SetChargingLimitAction", automation.Action)
StartDrivingAction = tesla_ble_vehicle_ns.class_("StartDrivingAction", automation.Action)

# Configuration constants
CONF_VIN = "vin"
CONF_CHARGING_AMPS_MAX = "charging_amps_max"
CONF_ROLE = "role"

CONF_VCSEC_POLL_INTERVAL = "vcsec_poll_interval"
CONF_INFOTAINMENT_POLL_INTERVAL_AWAKE = "infotainment_poll_interval_awake"
CONF_INFOTAINMENT_POLL_INTERVAL_ACTIVE = "infotainment_poll_interval_active"
CONF_INFOTAINMENT_SLEEP_TIMEOUT = "infotainment_sleep_timeout"

TESLA_ROLES = {
    "OWNER": "Keys_Role_ROLE_OWNER",
    "DRIVER": "Keys_Role_ROLE_DRIVER",
    "CHARGING_MANAGER": "Keys_Role_ROLE_CHARGING_MANAGER",
}

# =============================================================================
# ENTITY DEFINITIONS (所有自动实体均标记为 internal: True)
# =============================================================================

BINARY_SENSORS = [
    {"id": "asleep", "name": "Asleep", "icon": "mdi:sleep", "internal": True},
    {"id": "user_present", "name": "User Present", "icon": "mdi:account-check", "device_class": "occupancy", "internal": True},
    {"id": "charger", "name": "Charger", "icon": "mdi:power-plug", "device_class": "plug", "internal": True},
    {"id": "parking_brake", "name": "Parking Brake", "icon": "mdi:car-brake-parking", "internal": True},
    {"id": "door_driver_front", "name": "Door Driver Front", "icon": "mdi:car-door", "device_class": "door", "disabled_by_default": True, "internal": True},
    {"id": "door_driver_rear", "name": "Door Driver Rear", "icon": "mdi:car-door", "device_class": "door", "disabled_by_default": True, "internal": True},
    {"id": "door_passenger_front", "name": "Door Passenger Front", "icon": "mdi:car-door", "device_class": "door", "disabled_by_default": True, "internal": True},
    {"id": "door_passenger_rear", "name": "Door Passenger Rear", "icon": "mdi:car-door", "device_class": "door", "disabled_by_default": True, "internal": True},
    {"id": "window_driver_front", "name": "Window Driver Front", "icon": "mdi:car-window-side", "device_class": "window", "disabled_by_default": True, "internal": True},
    {"id": "window_driver_rear", "name": "Window Driver Rear", "icon": "mdi:car-window-side", "device_class": "window", "disabled_by_default": True, "internal": True},
    {"id": "window_passenger_front", "name": "Window Passenger Front", "icon": "mdi:car-window-side", "device_class": "window", "disabled_by_default": True, "internal": True},
    {"id": "window_passenger_rear", "name": "Window Passenger Rear", "icon": "mdi:car-window-side", "device_class": "window", "disabled_by_default": True, "internal": True},
    {"id": "sunroof", "name": "Sunroof", "icon": "mdi:car-select", "device_class": "window", "disabled_by_default": True, "internal": True},
]

SENSORS = [
    {"id": "battery_level", "name": "Battery", "icon": "mdi:battery", "unit": "%", "internal": True},
    {"id": "range", "name": "Range", "icon": "mdi:map-marker-distance", "device_class": "distance", "unit": "mi", "internal": True},
    {"id": "charger_power", "name": "Charger Power", "icon": "mdi:flash", "device_class": "power", "unit": "kW", "internal": True},
    {"id": "charger_voltage", "name": "Charger Voltage", "icon": "mdi:lightning-bolt", "device_class": "voltage", "unit": "V", "internal": True},
    {"id": "charger_current", "name": "Charger Current", "icon": "mdi:current-ac", "device_class": "current", "unit": "A", "internal": True},
    {"id": "charging_rate", "name": "Charging Rate", "icon": "mdi:speedometer", "device_class": "speed", "unit": "mph", "accuracy_decimals": 1, "internal": True},
    {"id": "energy_added", "name": "Energy Added", "icon": "mdi:battery-charging", "device_class": "energy", "unit": "kWh", "accuracy_decimals": 1, "internal": True},
    {"id": "time_to_full", "name": "Time to Full", "icon": "mdi:clock-outline", "device_class": "duration", "unit": "min", "internal": True},
    {"id": "outside_temp", "name": "Outside Temperature", "icon": "mdi:thermometer", "device_class": "temperature", "unit": "°C", "accuracy_decimals": 1, "internal": True},
    {"id": "odometer", "name": "Odometer", "icon": "mdi:counter", "device_class": "distance", "unit": "mi", "disabled_by_default": True, "internal": True},
    {"id": "tpms_front_left", "name": "TPMS Front Left", "icon": "mdi:car-tire-alert", "device_class": "pressure", "unit": "bar", "accuracy_decimals": 1, "internal": True},
    {"id": "tpms_front_right", "name": "TPMS Front Right", "icon": "mdi:car-tire-alert", "device_class": "pressure", "unit": "bar", "accuracy_decimals": 1, "internal": True},
    {"id": "tpms_rear_left", "name": "TPMS Rear Left", "icon": "mdi:car-tire-alert", "device_class": "pressure", "unit": "bar", "accuracy_decimals": 1, "internal": True},
    {"id": "tpms_rear_right", "name": "TPMS Rear Right", "icon": "mdi:car-tire-alert", "device_class": "pressure", "unit": "bar", "accuracy_decimals": 1, "internal": True},
]

TEXT_SENSORS = [
    {"id": "charging_state", "name": "Charging", "icon": "mdi:ev-station", "internal": True},
    {"id": "iec61851_state", "name": "IEC 61851", "icon": "mdi:ev-plug-type2", "disabled_by_default": True, "internal": True},
    {"id": "shift_state", "name": "Shift State", "icon": "mdi:car-shift-pattern", "disabled_by_default": True, "internal": True},
]

BUTTONS = [
    {"id": "wake", "name": "Wake up", "class": TeslaWakeButton, "setter": "set_wake_button", "icon": "mdi:sleep-off", "internal": True},
    {"id": "pair", "name": "Pair BLE Key", "class": TeslaPairButton, "setter": "set_pair_button", "icon": "mdi:key-wireless", "entity_category": "diagnostic", "internal": True},
    {"id": "regenerate_key", "name": "Regenerate key", "class": TeslaRegenerateKeyButton, "setter": "set_regenerate_key_button", "icon": "mdi:key-change", "entity_category": "diagnostic", "disabled_by_default": True, "internal": True},
    {"id": "force_update", "name": "Force data update", "class": TeslaForceUpdateButton, "setter": "set_force_update_button", "icon": "mdi:database-sync", "entity_category": "diagnostic", "internal": True},
    {"id": "unlatch_driver_door", "name": "Unlatch Driver Door", "class": TeslaUnlatchDriverDoorButton, "setter": None, "icon": "mdi:car-door", "disabled_by_default": True, "internal": True},
    {"id": "flash_lights", "name": "Flash Lights", "class": TeslaFlashLightsButton, "setter": None, "icon": "mdi:car-light-high", "internal": True},
    {"id": "honk_horn", "name": "Sound Horn", "class": TeslaHonkHornButton, "setter": None, "icon": "mdi:bullhorn", "internal": True},
    {"id": "start_driving", "name": "Start Driving", "class": TeslaStartDrivingButton, "setter": "set_start_driving_button", "icon": "mdi:car-key", "internal": True},
]

SWITCHES = [
    {"id": "charging", "name": "Charger", "class": TeslaChargingSwitch, "setter": "set_charging_switch", "icon": "mdi:ev-station", "internal": True},
    {"id": "steering_wheel_heat", "name": "Heated Steering", "class": TeslaSteeringWheelHeatSwitch, "setter": "set_steering_wheel_heat_switch", "icon": "mdi:steering", "internal": True},
    {"id": "sentry_mode", "name": "Sentry Mode", "class": TeslaSentryModeSwitch, "setter": "set_sentry_mode_switch", "icon": "mdi:shield-car", "internal": True},
]

LOCKS = [
    {"id": "doors", "name": "Doors", "class": TeslaDoorsLock, "setter": "set_doors_lock", "icon": "mdi:car-door-lock", "internal": True},
    {"id": "charge_port_latch", "name": "Charge Port Latch", "class": TeslaChargePortLatchLock, "setter": "set_charge_port_latch_lock", "icon": "mdi:ev-plug-tesla", "internal": True},
]

COVERS = [
    {"id": "trunk", "name": "Trunk", "class": TeslaTrunkCover, "setter": "set_trunk_cover", "icon": "mdi:car-back", "device_class": "door", "internal": True},
    {"id": "frunk", "name": "Frunk", "class": TeslaFrunkCover, "setter": "set_frunk_cover", "icon": "mdi:car", "device_class": "door", "internal": True},
    {"id": "windows", "name": "Windows", "class": TeslaWindowsCover, "setter": "set_windows_cover", "icon": "mdi:car-door", "device_class": "awning", "internal": True},
    {"id": "charge_port_door", "name": "Charge Port Door", "class": TeslaChargePortDoorCover, "setter": "set_charge_port_door_cover", "icon": "mdi:ev-plug-tesla", "device_class": "door", "internal": True},
]

CLIMATE = {
    "id": "climate", "name": "Climate", "class": TeslaClimate, "setter": "set_climate", "internal": True,
}

NUMBERS = [
    {"id": "charging_amps", "name": "Charging Amps", "class": TeslaChargingAmpsNumber, "setter": "set_charging_amps_number", "icon": "mdi:current-ac", "unit": "A", "min": 0, "max": "config", "step": 1, "internal": True},
    {"id": "charging_limit", "name": "Charging Limit", "class": TeslaChargingLimitNumber, "setter": "set_charging_limit_number", "icon": "mdi:battery-charging-100", "unit": "%", "min": 50, "max": 100, "step": 1, "internal": True},
]

# =============================================================================
# CONFIG SCHEMA (扩展用户自定义传感器选项)
# =============================================================================

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_ID): cv.declare_id(TeslaBLEVehicle),
            cv.Required(CONF_VIN): cv.string,
            cv.Optional(CONF_CHARGING_AMPS_MAX, default=32): cv.int_range(min=1, max=48),
            cv.Optional(CONF_ROLE, default="DRIVER"): cv.enum(TESLA_ROLES, upper=True),
            cv.Optional(CONF_VCSEC_POLL_INTERVAL, default=10): cv.int_range(min=5, max=300),
            cv.Optional(CONF_INFOTAINMENT_POLL_INTERVAL_AWAKE, default=30): cv.int_range(min=10, max=600),
            cv.Optional(CONF_INFOTAINMENT_POLL_INTERVAL_ACTIVE, default=10): cv.int_range(min=5, max=120),
            cv.Optional(CONF_INFOTAINMENT_SLEEP_TIMEOUT, default=660): cv.int_range(min=60, max=3600),

            # ★ 用户自定义数值传感器 (可选) — 已扩展
            cv.Optional("battery_level"): sensor.sensor_schema(unit_of_measurement="%", accuracy_decimals=0),
            cv.Optional("range"): sensor.sensor_schema(unit_of_measurement="mi", device_class="distance", accuracy_decimals=0),          # 新增
            cv.Optional("range_rated_api"): sensor.sensor_schema(unit_of_measurement="km", accuracy_decimals=1),
            cv.Optional("inside_temp"): sensor.sensor_schema(unit_of_measurement="°C", device_class="temperature", accuracy_decimals=1),
            cv.Optional("outside_temp"): sensor.sensor_schema(unit_of_measurement="°C", device_class="temperature", accuracy_decimals=1),
            cv.Optional("driver_temp_setting"): sensor.sensor_schema(unit_of_measurement="°C", device_class="temperature", accuracy_decimals=1),
            cv.Optional("passenger_temp_setting"): sensor.sensor_schema(unit_of_measurement="°C", device_class="temperature", accuracy_decimals=1),
            cv.Optional("odometer"): sensor.sensor_schema(unit_of_measurement="km", device_class="distance", accuracy_decimals=1),
            cv.Optional("speed"): sensor.sensor_schema(unit_of_measurement="km/h", device_class="speed", accuracy_decimals=1),
            cv.Optional("charge_energy_added"): sensor.sensor_schema(unit_of_measurement="kWh", device_class="energy", accuracy_decimals=2),
            cv.Optional("charge_rate"): sensor.sensor_schema(unit_of_measurement="km/h", accuracy_decimals=1),
            cv.Optional("charger_power"): sensor.sensor_schema(unit_of_measurement="kW", device_class="power", accuracy_decimals=0),
            cv.Optional("charger_voltage"): sensor.sensor_schema(unit_of_measurement="V", device_class="voltage", accuracy_decimals=0),  # 新增
            cv.Optional("charger_current"): sensor.sensor_schema(unit_of_measurement="A", device_class="current", accuracy_decimals=1),  # 新增
            cv.Optional("charging_rate"): sensor.sensor_schema(unit_of_measurement="mph", device_class="speed", accuracy_decimals=1),    # 新增
            cv.Optional("time_to_full_charge"): sensor.sensor_schema(unit_of_measurement="min", device_class="duration", accuracy_decimals=0),
            cv.Optional("tpms_front_left"): sensor.sensor_schema(unit_of_measurement="bar", device_class="pressure", accuracy_decimals=1),   # 新增
            cv.Optional("tpms_front_right"): sensor.sensor_schema(unit_of_measurement="bar", device_class="pressure", accuracy_decimals=1),  # 新增
            cv.Optional("tpms_rear_left"): sensor.sensor_schema(unit_of_measurement="bar", device_class="pressure", accuracy_decimals=1),    # 新增
            cv.Optional("tpms_rear_right"): sensor.sensor_schema(unit_of_measurement="bar", device_class="pressure", accuracy_decimals=1),   # 新增

            # ★ 用户自定义二进制传感器 (可选)
            cv.Optional("locked"): binary_sensor.binary_sensor_schema(device_class="lock"),
            cv.Optional("user_present"): binary_sensor.binary_sensor_schema(device_class="presence"),
            cv.Optional("charge_flap_open"): binary_sensor.binary_sensor_schema(device_class="opening"),
            cv.Optional("asleep"): binary_sensor.binary_sensor_schema(),
            cv.Optional("charging"): binary_sensor.binary_sensor_schema(device_class="battery_charging"),

            # ★ 用户自定义文本传感器 (可选)
            cv.Optional("shift_state"): text_sensor.text_sensor_schema(),
            cv.Optional("charging_state"): text_sensor.text_sensor_schema(),
            cv.Optional("iec61851_state"): text_sensor.text_sensor_schema(),
        },
    )
    .extend(cv.polling_component_schema("10s"))
    .extend(ble_client.BLE_CLIENT_SCHEMA)
)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_device_class_const(component_module, device_class_str):
    if device_class_str is None:
        return None
    return getattr(component_module, f"DEVICE_CLASS_{device_class_str.upper()}", None)

async def create_binary_sensor(var, definition, user_config=None):
    if user_config:
        bs = await binary_sensor.new_binary_sensor(user_config)
    else:
        config = {
            CONF_ID: cv.declare_id(binary_sensor.BinarySensor)(f"tesla_{definition['id']}_sensor"),
            CONF_NAME: definition["name"],
            CONF_DISABLED_BY_DEFAULT: definition.get("disabled_by_default", False),
        }
        if "icon" in definition: config[CONF_ICON] = definition["icon"]
        if "device_class" in definition:
            dc = get_device_class_const(binary_sensor, definition["device_class"])
            if dc: config[CONF_DEVICE_CLASS] = dc
        if definition.get("internal"):
            config[CONF_INTERNAL] = True
        bs = await binary_sensor.new_binary_sensor(config)
    cg.add(var.set_binary_sensor(definition["id"], bs))
    return bs

async def create_sensor(var, definition, user_config=None):
    if user_config:
        sens = await sensor.new_sensor(user_config)
    else:
        config = {
            CONF_ID: cv.declare_id(sensor.Sensor)(f"tesla_{definition['id']}_sensor"),
            CONF_NAME: definition["name"],
            CONF_DISABLED_BY_DEFAULT: definition.get("disabled_by_default", False),
            CONF_FORCE_UPDATE: False,
        }
        if "icon" in definition: config[CONF_ICON] = definition["icon"]
        if "unit" in definition: config[CONF_UNIT_OF_MEASUREMENT] = definition["unit"]
        if "accuracy_decimals" in definition: config[CONF_ACCURACY_DECIMALS] = definition["accuracy_decimals"]
        if "device_class" in definition:
            dc = get_device_class_const(sensor, definition["device_class"])
            if dc: config[CONF_DEVICE_CLASS] = dc
        if definition.get("internal"):
            config[CONF_INTERNAL] = True
        sens = await sensor.new_sensor(config)
    cg.add(var.set_sensor(definition["id"], sens))
    return sens

async def create_text_sensor(var, definition, user_config=None):
    if user_config:
        ts = await text_sensor.new_text_sensor(user_config)
    else:
        config = {
            CONF_ID: cv.declare_id(text_sensor.TextSensor)(f"tesla_{definition['id']}_sensor"),
            CONF_NAME: definition["name"],
            CONF_DISABLED_BY_DEFAULT: definition.get("disabled_by_default", False),
            CONF_FORCE_UPDATE: False,
        }
        if "icon" in definition: config[CONF_ICON] = definition["icon"]
        if definition.get("internal"):
            config[CONF_INTERNAL] = True
        ts = await text_sensor.new_text_sensor(config)
    cg.add(var.set_text_sensor(definition["id"], ts))
    return ts

async def create_button(var, definition):
    config = {
        CONF_ID: cv.declare_id(definition["class"])(f"tesla_{definition['id']}_button"),
        CONF_NAME: definition["name"],
        CONF_DISABLED_BY_DEFAULT: definition.get("disabled_by_default", False),
    }
    if "icon" in definition: config[CONF_ICON] = definition["icon"]
    if "entity_category" in definition:
        if definition["entity_category"] == "diagnostic":
            config[CONF_ENTITY_CATEGORY] = cg.EntityCategory.ENTITY_CATEGORY_DIAGNOSTIC
    if definition.get("internal"):
        config[CONF_INTERNAL] = True
    btn = await button.new_button(config)
    cg.add(btn.set_parent(var))
    if definition.get("setter"):
        cg.add(getattr(var, definition["setter"])(btn))
    return btn

async def create_switch(var, definition):
    config = {
        CONF_ID: cv.declare_id(definition["class"])(f"tesla_{definition['id']}_switch"),
        CONF_NAME: definition["name"],
        CONF_DISABLED_BY_DEFAULT: definition.get("disabled_by_default", False),
        CONF_RESTORE_MODE: switch.RESTORE_MODES['RESTORE_DEFAULT_OFF'],
    }
    if "icon" in definition: config[CONF_ICON] = definition["icon"]
    if definition.get("internal"):
        config[CONF_INTERNAL] = True
    sw = await switch.new_switch(config)
    cg.add(sw.set_parent(var))
    if definition.get("setter"):
        cg.add(getattr(var, definition["setter"])(sw))
    return sw

async def create_number(var, definition, config):
    max_val = definition["max"]
    if max_val == "config": max_val = config.get(CONF_CHARGING_AMPS_MAX, 32)
    num_config = {
        CONF_ID: cv.declare_id(definition["class"])(f"tesla_{definition['id']}_number"),
        CONF_NAME: definition["name"],
        CONF_DISABLED_BY_DEFAULT: definition.get("disabled_by_default", False),
        CONF_MODE: number.NUMBER_MODES['AUTO'],
    }
    if "icon" in definition: num_config[CONF_ICON] = definition["icon"]
    if "unit" in definition: num_config[CONF_UNIT_OF_MEASUREMENT] = definition["unit"]
    if definition.get("internal"):
        num_config[CONF_INTERNAL] = True
    num = await number.new_number(num_config, min_value=definition["min"], max_value=max_val, step=definition["step"])
    cg.add(num.set_parent(var))
    if definition.get("setter"): cg.add(getattr(var, definition["setter"])(num))
    return num

async def create_lock(var, definition):
    config = {
        CONF_ID: cv.declare_id(definition["class"])(f"tesla_{definition['id']}_lock"),
        CONF_NAME: definition["name"],
        CONF_DISABLED_BY_DEFAULT: definition.get("disabled_by_default", False),
    }
    if "icon" in definition: config[CONF_ICON] = definition["icon"]
    if definition.get("internal"):
        config[CONF_INTERNAL] = True
    lck = cg.new_Pvariable(config[CONF_ID])
    await lock.register_lock(lck, config)
    cg.add(lck.set_parent(var))
    if definition.get("setter"): cg.add(getattr(var, definition["setter"])(lck))
    return lck

async def create_cover(var, definition):
    config = {
        CONF_ID: cv.declare_id(definition["class"])(f"tesla_{definition['id']}_cover"),
        CONF_NAME: definition["name"],
        CONF_DISABLED_BY_DEFAULT: definition.get("disabled_by_default", False),
    }
    if "icon" in definition: config[CONF_ICON] = definition["icon"]
    if "device_class" in definition: config[CONF_DEVICE_CLASS] = definition["device_class"]
    if definition.get("internal"):
        config[CONF_INTERNAL] = True
    cvr = cg.new_Pvariable(config[CONF_ID])
    await cover.register_cover(cvr, config)
    cg.add(cvr.set_parent(var))
    if definition.get("setter"): cg.add(getattr(var, definition["setter"])(cvr))
    return cvr

async def create_climate_entity(var, definition):
    from esphome.components.climate import CONF_VISUAL
    config = {
        CONF_ID: cv.declare_id(definition["class"])(f"tesla_{definition['id']}_climate"),
        CONF_NAME: definition["name"],
        CONF_DISABLED_BY_DEFAULT: False,
        CONF_VISUAL: {},
        CONF_ACCURACY_DECIMALS: 1,
    }
    if definition.get("internal"):
        config[CONF_INTERNAL] = True
    clm = cg.new_Pvariable(config[CONF_ID])
    await climate.register_climate(clm, config)
    cg.add(clm.set_parent(var))
    if definition.get("setter"): cg.add(getattr(var, definition["setter"])(clm))
    return clm

# =============================================================================
# CODE GENERATION (修改 to_code 以达到不重复创建)
# =============================================================================

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await ble_client.register_ble_node(var, config)
    cg.add(var.set_vin(config[CONF_VIN]))
    role = config[CONF_ROLE]
    charging_amps_max = config[CONF_CHARGING_AMPS_MAX]
    vcsec_interval_seconds = config[CONF_VCSEC_POLL_INTERVAL]

    cg.add(var.set_update_interval(vcsec_interval_seconds * 1000))
    cg.add(var.set_role(TESLA_ROLES[role]))
    cg.add(var.set_charging_amps_max(charging_amps_max))
    cg.add(var.set_vcsec_poll_interval(vcsec_interval_seconds * 1000))
    cg.add(var.set_infotainment_poll_interval_awake(config[CONF_INFOTAINMENT_POLL_INTERVAL_AWAKE] * 1000))
    cg.add(var.set_infotainment_poll_interval_active(config[CONF_INFOTAINMENT_POLL_INTERVAL_ACTIVE] * 1000))
    cg.add(var.set_infotainment_sleep_timeout(config[CONF_INFOTAINMENT_SLEEP_TIMEOUT] * 1000))

    # 记录用户显式配置了哪些传感器键，避免与原有列表重复创建
    user_sensor_keys = set()
    user_binary_keys = set()
    user_text_keys = set()

    # 扩展 user_sensor_keys，包含新增的传感器
    for skey in ["battery_level", "range", "range_rated_api", "inside_temp", "outside_temp",
                 "driver_temp_setting", "passenger_temp_setting", "odometer", "speed",
                 "charge_energy_added", "charge_rate", "charger_power", "charger_voltage",
                 "charger_current", "charging_rate", "time_to_full_charge",
                 "tpms_front_left", "tpms_front_right", "tpms_rear_left", "tpms_rear_right"]:
        if skey in config:
            user_sensor_keys.add(skey)

    for bkey in ["locked", "user_present", "charge_flap_open", "asleep", "charging"]:
        if bkey in config:
            user_binary_keys.add(bkey)

    for tkey in ["shift_state", "charging_state", "iec61851_state"]:
        if tkey in config:
            user_text_keys.add(tkey)

    skip_binary_ids = set()
    if "user_present" in user_binary_keys:
        skip_binary_ids.add("user_present")
    if "asleep" in user_binary_keys:
        skip_binary_ids.add("asleep")

    # 扩展 skip_sensor_ids，包含所有用户可能显式定义的传感器 ID
    skip_sensor_ids = set()
    id_map = {
        "battery_level": "battery_level",
        "range": "range",
        "range_rated_api": "range_rated_api",
        "inside_temp": "inside_temp",
        "outside_temp": "outside_temp",
        "driver_temp_setting": "driver_temp_setting",
        "passenger_temp_setting": "passenger_temp_setting",
        "odometer": "odometer",
        "speed": "speed",
        "charge_energy_added": "charge_energy_added",
        "charge_rate": "charge_rate",
        "charger_power": "charger_power",
        "charger_voltage": "charger_voltage",
        "charger_current": "charger_current",
        "charging_rate": "charging_rate",
        "time_to_full_charge": "time_to_full_charge",
        "tpms_front_left": "tpms_front_left",
        "tpms_front_right": "tpms_front_right",
        "tpms_rear_left": "tpms_rear_left",
        "tpms_rear_right": "tpms_rear_right",
    }
    for config_key, sensor_id in id_map.items():
        if config_key in user_sensor_keys:
            skip_sensor_ids.add(sensor_id)

    skip_text_ids = set()
    if "shift_state" in user_text_keys:
        skip_text_ids.add("shift_state")
    if "charging_state" in user_text_keys:
        skip_text_ids.add("charging_state")
    if "iec61851_state" in user_text_keys:
        skip_text_ids.add("iec61851_state")

    for definition in BINARY_SENSORS:
        if definition["id"] not in skip_binary_ids:
            await create_binary_sensor(var, definition)
    for definition in SENSORS:
        if definition["id"] not in skip_sensor_ids:
            await create_sensor(var, definition)
    for definition in TEXT_SENSORS:
        if definition["id"] not in skip_text_ids:
            await create_text_sensor(var, definition)

    # 用户显式定义的传感器（使用用户提供的配置）
    # 原有传感器
    if "battery_level" in config:
        await create_sensor(var, {"id": "battery_level"}, user_config=config["battery_level"])
    if "range" in config:
        await create_sensor(var, {"id": "range"}, user_config=config["range"])
    if "range_rated_api" in config:
        await create_sensor(var, {"id": "range_rated_api"}, user_config=config["range_rated_api"])
    if "inside_temp" in config:
        await create_sensor(var, {"id": "inside_temp"}, user_config=config["inside_temp"])
    if "outside_temp" in config:
        await create_sensor(var, {"id": "outside_temp"}, user_config=config["outside_temp"])
    if "driver_temp_setting" in config:
        await create_sensor(var, {"id": "driver_temp_setting"}, user_config=config["driver_temp_setting"])
    if "passenger_temp_setting" in config:
        await create_sensor(var, {"id": "passenger_temp_setting"}, user_config=config["passenger_temp_setting"])
    if "odometer" in config:
        await create_sensor(var, {"id": "odometer"}, user_config=config["odometer"])
    if "speed" in config:
        await create_sensor(var, {"id": "speed"}, user_config=config["speed"])
    if "charge_energy_added" in config:
        await create_sensor(var, {"id": "charge_energy_added"}, user_config=config["charge_energy_added"])
    if "charge_rate" in config:
        await create_sensor(var, {"id": "charge_rate"}, user_config=config["charge_rate"])
    if "charger_power" in config:
        await create_sensor(var, {"id": "charger_power"}, user_config=config["charger_power"])
    if "charger_voltage" in config:
        await create_sensor(var, {"id": "charger_voltage"}, user_config=config["charger_voltage"])
    if "charger_current" in config:
        await create_sensor(var, {"id": "charger_current"}, user_config=config["charger_current"])
    if "charging_rate" in config:
        await create_sensor(var, {"id": "charging_rate"}, user_config=config["charging_rate"])
    if "time_to_full_charge" in config:
        await create_sensor(var, {"id": "time_to_full_charge"}, user_config=config["time_to_full_charge"])
    if "tpms_front_left" in config:
        await create_sensor(var, {"id": "tpms_front_left"}, user_config=config["tpms_front_left"])
    if "tpms_front_right" in config:
        await create_sensor(var, {"id": "tpms_front_right"}, user_config=config["tpms_front_right"])
    if "tpms_rear_left" in config:
        await create_sensor(var, {"id": "tpms_rear_left"}, user_config=config["tpms_rear_left"])
    if "tpms_rear_right" in config:
        await create_sensor(var, {"id": "tpms_rear_right"}, user_config=config["tpms_rear_right"])

    # 二进制传感器
    if "locked" in config:
        await create_binary_sensor(var, {"id": "locked"}, user_config=config["locked"])
    if "user_present" in config:
        await create_binary_sensor(var, {"id": "user_present"}, user_config=config["user_present"])
    if "charge_flap_open" in config:
        await create_binary_sensor(var, {"id": "charge_flap_open"}, user_config=config["charge_flap_open"])
    if "asleep" in config:
        await create_binary_sensor(var, {"id": "asleep"}, user_config=config["asleep"])
    if "charging" in config:
        await create_binary_sensor(var, {"id": "charging"}, user_config=config["charging"])

    # 文本传感器
    if "shift_state" in config:
        await create_text_sensor(var, {"id": "shift_state"}, user_config=config["shift_state"])
    if "charging_state" in config:
        await create_text_sensor(var, {"id": "charging_state"}, user_config=config["charging_state"])
    if "iec61851_state" in config:
        await create_text_sensor(var, {"id": "iec61851_state"}, user_config=config["iec61851_state"])

    # 其余实体（按钮、开关等）
    for definition in BUTTONS: await create_button(var, definition)
    for definition in SWITCHES: await create_switch(var, definition)
    for definition in NUMBERS: await create_number(var, definition, config)
    for definition in LOCKS: await create_lock(var, definition)
    for definition in COVERS: await create_cover(var, definition)
    await create_climate_entity(var, CLIMATE)

# =============================================================================
# ACTION REGISTRATION (不变)
# =============================================================================

TESLA_WAKE_ACTION_SCHEMA = cv.Schema({cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle)})
TESLA_PAIR_ACTION_SCHEMA = cv.Schema({cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle)})
TESLA_REGENERATE_KEY_ACTION_SCHEMA = cv.Schema({cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle)})
TESLA_FORCE_UPDATE_ACTION_SCHEMA = cv.Schema({cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle)})
TESLA_SET_CHARGING_ACTION_SCHEMA = cv.Schema({cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle), cv.Required("state"): cv.templatable(cv.boolean)})
TESLA_SET_CHARGING_AMPS_ACTION_SCHEMA = cv.Schema({cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle), cv.Required("amps"): cv.templatable(cv.int_range(min=0, max=80))})
TESLA_SET_CHARGING_LIMIT_ACTION_SCHEMA = cv.Schema({cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle), cv.Required("limit"): cv.templatable(cv.int_range(min=50, max=100))})

@automation.register_action("tesla_ble_vehicle.wake", WakeAction, TESLA_WAKE_ACTION_SCHEMA)
async def tesla_wake_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, paren)

@automation.register_action("tesla_ble_vehicle.pair", PairAction, TESLA_PAIR_ACTION_SCHEMA)
async def tesla_pair_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, paren)

@automation.register_action("tesla_ble_vehicle.regenerate_key", RegenerateKeyAction, TESLA_REGENERATE_KEY_ACTION_SCHEMA)
async def tesla_regenerate_key_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, paren)

@automation.register_action("tesla_ble_vehicle.force_update", ForceUpdateAction, TESLA_FORCE_UPDATE_ACTION_SCHEMA)
async def tesla_force_update_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, paren)

@automation.register_action("tesla_ble_vehicle.set_charging", SetChargingAction, TESLA_SET_CHARGING_ACTION_SCHEMA)
async def tesla_set_charging_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config["state"], args, bool)
    cg.add(var.set_state(template_))
    return var

@automation.register_action("tesla_ble_vehicle.set_charging_amps", SetChargingAmpsAction, TESLA_SET_CHARGING_AMPS_ACTION_SCHEMA)
async def tesla_set_charging_amps_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config["amps"], args, int)
    cg.add(var.set_amps(template_))
    return var

@automation.register_action("tesla_ble_vehicle.set_charging_limit", SetChargingLimitAction, TESLA_SET_CHARGING_LIMIT_ACTION_SCHEMA)
async def tesla_set_charging_limit_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config["limit"], args, int)
    cg.add(var.set_limit(template_))
    return var

TESLA_START_DRIVING_ACTION_SCHEMA = cv.Schema({
    cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle),
})

@automation.register_action(
    "tesla_ble_vehicle.start_driving",
    StartDrivingAction,
    TESLA_START_DRIVING_ACTION_SCHEMA,
)
async def tesla_start_driving_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])   
    return cg.new_Pvariable(action_id, template_arg, paren)
