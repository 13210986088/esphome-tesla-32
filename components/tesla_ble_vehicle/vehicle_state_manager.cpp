#include "vehicle_state_manager.h"
#include "tesla_ble_vehicle.h"
#include <esphome/core/helpers.h>
#include <cmath>
#include <algorithm>

namespace esphome {
namespace tesla_ble_vehicle {

VehicleStateManager::VehicleStateManager(TeslaBLEVehicle* parent)
    : parent_(parent) {}

void VehicleStateManager::set_binary_sensor(const std::string& id, binary_sensor::BinarySensor* sensor) {
    if (sensor == nullptr) {
        return;
    }
    binary_sensors_[id] = sensor;
    ESP_LOGD(STATE_MANAGER_TAG, "Registered binary sensor: %s", id.c_str());
}

void VehicleStateManager::set_sensor(const std::string& id, sensor::Sensor* sensor) {
    if (sensor == nullptr) {
        return;
    }
    sensors_[id] = sensor;
    ESP_LOGD(STATE_MANAGER_TAG, "Registered sensor: %s", id.c_str());
}

void VehicleStateManager::set_text_sensor(const std::string& id, text_sensor::TextSensor* sensor) {
    if (sensor == nullptr) {
        return;
    }
    text_sensors_[id] = sensor;
    ESP_LOGD(STATE_MANAGER_TAG, "Registered text sensor: %s", id.c_str());
}

binary_sensor::BinarySensor* VehicleStateManager::get_binary_sensor(const std::string& id) {
    auto it = binary_sensors_.find(id);
    return (it != binary_sensors_.end()) ? it->second : nullptr;
}

sensor::Sensor* VehicleStateManager::get_sensor(const std::string& id) {
    auto it = sensors_.find(id);
    return (it != sensors_.end()) ? it->second : nullptr;
}

text_sensor::TextSensor* VehicleStateManager::get_text_sensor(const std::string& id) {
    auto it = text_sensors_.find(id);
    return (it != text_sensors_.end()) ? it->second : nullptr;
}

void VehicleStateManager::publish_sensor(const std::string& id, float value) {
    auto* sensor = get_sensor(id);
    if (sensor != nullptr) {
        sensor->publish_state(value);
        ESP_LOGD(STATE_MANAGER_TAG, "Published sensor %s: %.2f", id.c_str(), value);
    }
}

void VehicleStateManager::publish_binary_sensor(const std::string& id, bool state) {
    auto* sensor = get_binary_sensor(id);
    if (sensor != nullptr) {
        sensor->publish_state(state);
        ESP_LOGD(STATE_MANAGER_TAG, "Published binary sensor %s: %s", id.c_str(), state ? "true" : "false");
    }
}

void VehicleStateManager::publish_text_sensor(const std::string& id, const std::string& value) {
    auto* sensor = get_text_sensor(id);
    if (sensor != nullptr) {
        sensor->publish_state(value);
        ESP_LOGD(STATE_MANAGER_TAG, "Published text sensor %s: %s", id.c_str(), value.c_str());
    }
}

void VehicleStateManager::update_charge_state(const CarServer_ChargeState& charge_state) {
    // 处理充电状态更新
    ESP_LOGD(STATE_MANAGER_TAG, "Updating charge state");
    
    if (charge_state.which_optional_charger_voltage) {
        const float voltage = static_cast<float>(charge_state.optional_charger_voltage.charger_voltage);
        if (voltage >= 0.0f && voltage <= 500.0f && std::isfinite(voltage)) {
            publish_sensor("charger_voltage", voltage);
        }
    }
    
    if (charge_state.which_optional_charger_actual_current) {
        const float current = static_cast<float>(charge_state.optional_charger_actual_current.charger_actual_current);
        if (current >= 0.0f && current <= 500.0f && std::isfinite(current)) {
            publish_sensor("charger_current", current);
        }
    }
    
    if (charge_state.which_optional_charger_power) {
        const float power_kw = static_cast<float>(charge_state.optional_charger_power.charger_power);
        if (power_kw >= 0.0f && power_kw <= 500.0f && std::isfinite(power_kw)) {
            publish_sensor("charger_power", power_kw);
        }
    }
    
    if (charge_state.which_optional_battery_range) {
        const float range = charge_state.optional_battery_range.battery_range;
        if (range >= 0.0f && range <= 500.0f && std::isfinite(range)) {
            publish_sensor("range", range);
        }
    }
    
    // 注意：range_rated_api 字段在 CarServer_ChargeState 中不存在，已删除
    
    if (charge_state.which_optional_charge_energy_added) {
        const float energy = charge_state.optional_charge_energy_added.charge_energy_added;
        if (energy >= 0.0f && std::isfinite(energy)) {
            publish_sensor("charge_energy_added", energy);
        }
    }
    
    if (charge_state.which_optional_minutes_to_full_charge) {
        const float minutes = static_cast<float>(charge_state.optional_minutes_to_full_charge.minutes_to_full_charge);
        if (minutes >= 0.0f && std::isfinite(minutes)) {
            publish_sensor("time_to_full_charge", minutes);
        }
    }
    
    if (charge_state.which_optional_charge_rate_mph) {
        const float rate = charge_state.optional_charge_rate_mph.charge_rate_mph;
        if (rate >= 0.0f && std::isfinite(rate)) {
            publish_sensor("charging_rate", rate);
        }
    }
    
    // 处理充电状态文本
    if (charge_state.has_charging_state) {
        std::string state_str;
        switch (charge_state.charging_state) {
            case ChargeState_CHARGING_STATE_CHARGING:
                state_str = "Charging";
                break;
            case ChargeState_CHARGING_STATE_COMPLETE:
                state_str = "Complete";
                break;
            case ChargeState_CHARGING_STATE_DISCONNECTED:
                state_str = "Disconnected";
                break;
            case ChargeState_CHARGING_STATE_NO_POWER:
                state_str = "NoPower";
                break;
            case ChargeState_CHARGING_STATE_READY:
                state_str = "Ready";
                break;
            case ChargeState_CHARGING_STATE_STARTING:
                state_str = "Starting";
                break;
            case ChargeState_CHARGING_STATE_STOPPED:
                state_str = "Stopped";
                break;
            default:
                state_str = "Unknown";
                break;
        }
        publish_text_sensor("charging_state", state_str);
    }
    
    // 处理 IEC 61851 状态
    if (charge_state.has_iec61851_state) {
        std::string iec_str;
        switch (charge_state.iec61851_state) {
            case Iec61851State_IEC_61851_STATE_A:
                iec_str = "A";
                break;
            case Iec61851State_IEC_61851_STATE_B:
                iec_str = "B";
                break;
            case Iec61851State_IEC_61851_STATE_C:
                iec_str = "C";
                break;
            case Iec61851State_IEC_61851_STATE_D:
                iec_str = "D";
                break;
            case Iec61851State_IEC_61851_STATE_E:
                iec_str = "E";
                break;
            case Iec61851State_IEC_61851_STATE_F:
                iec_str = "F";
                break;
            default:
                iec_str = "Unknown";
                break;
        }
        publish_text_sensor("iec61851_state", iec_str);
    }
}

void VehicleStateManager::update_climate_state(const CarServer_ClimateState& climate_state) {
    ESP_LOGD(STATE_MANAGER_TAG, "Updating climate state");
    
    if (climate_state.which_optional_inside_temp) {
        const float temp = climate_state.optional_inside_temp.inside_temp;
        if (std::isfinite(temp) && temp > -50.0f && temp < 100.0f) {
            publish_sensor("inside_temp", temp);
        }
    }
    
    if (climate_state.which_optional_outside_temp) {
        const float temp = climate_state.optional_outside_temp.outside_temp;
        if (std::isfinite(temp) && temp > -50.0f && temp < 100.0f) {
            publish_sensor("outside_temp", temp);
        }
    }
    
    if (climate_state.which_optional_driver_temp_setting) {
        const float temp = climate_state.optional_driver_temp_setting.driver_temp_setting;
        if (std::isfinite(temp) && temp > 0.0f && temp < 50.0f) {
            publish_sensor("driver_temp_setting", temp);
        }
    }
    
    if (climate_state.which_optional_passenger_temp_setting) {
        const float temp = climate_state.optional_passenger_temp_setting.passenger_temp_setting;
        if (std::isfinite(temp) && temp > 0.0f && temp < 50.0f) {
            publish_sensor("passenger_temp_setting", temp);
        }
    }
}

void VehicleStateManager::update_vehicle_data(const CarServer_VehicleData& vehicle_data) {
    ESP_LOGD(STATE_MANAGER_TAG, "Updating vehicle data");
    
    // 处理充电状态
    if (vehicle_data.has_charge_state) {
        update_charge_state(vehicle_data.charge_state);
    }
    
    // 处理气候状态
    if (vehicle_data.has_climate_state) {
        update_climate_state(vehicle_data.climate_state);
    }
    
    // 处理驾驶状态
    if (vehicle_data.has_drive_state) {
        const auto& drive_state = vehicle_data.drive_state;
        
        if (drive_state.which_optional_speed) {
            const float speed = drive_state.optional_speed.speed;
            if (std::isfinite(speed) && speed >= 0.0f) {
                publish_sensor("speed", speed);
            }
        }
        
        if (drive_state.has_shift_state) {
            std::string shift_str;
            switch (drive_state.shift_state) {
                case ShiftState_SHIFT_STATE_P:
                    shift_str = "P";
                    break;
                case ShiftState_SHIFT_STATE_R:
                    shift_str = "R";
                    break;
                case ShiftState_SHIFT_STATE_N:
                    shift_str = "N";
                    break;
                case ShiftState_SHIFT_STATE_D:
                    shift_str = "D";
                    break;
                default:
                    shift_str = "Unknown";
                    break;
            }
            publish_text_sensor("shift_state", shift_str);
        }
    }
    
    // 处理车辆状态
    if (vehicle_data.has_vehicle_state) {
        const auto& vstate = vehicle_data.vehicle_state;
        
        if (vstate.which_optional_odometer) {
            const float odometer = vstate.optional_odometer.odometer;
            if (std::isfinite(odometer) && odometer >= 0.0f) {
                publish_sensor("odometer", odometer);
            }
        }
        
        // 门锁状态
        if (vstate.has_locked) {
            publish_binary_sensor("locked", vstate.locked);
        }
        
        // 用户在场状态
        if (vstate.has_user_present) {
            publish_binary_sensor("user_present", vstate.user_present);
        }
        
        // 充电口状态
        if (vstate.has_charge_port_door_open) {
            publish_binary_sensor("charge_flap_open", vstate.charge_port_door_open);
        }
    }
    
    // 处理胎压数据
    if (vehicle_data.has_tpms_state) {
        const auto& tpms = vehicle_data.tpms_state;
        
        if (tpms.which_optional_tpms_pressure_fl) {
            const float pressure = tpms.optional_tpms_pressure_fl.tpms_pressure_fl;
            if (std::isfinite(pressure) && pressure >= 0.0f) {
                publish_sensor("tpms_front_left", pressure);
            }
        }
        
        if (tpms.which_optional_tpms_pressure_fr) {
            const float pressure = tpms.optional_tpms_pressure_fr.tpms_pressure_fr;
            if (std::isfinite(pressure) && pressure >= 0.0f) {
                publish_sensor("tpms_front_right", pressure);
            }
        }
        
        if (tpms.which_optional_tpms_pressure_rl) {
            const float pressure = tpms.optional_tpms_pressure_rl.tpms_pressure_rl;
            if (std::isfinite(pressure) && pressure >= 0.0f) {
                publish_sensor("tpms_rear_left", pressure);
            }
        }
        
        if (tpms.which_optional_tpms_pressure_rr) {
            const float pressure = tpms.optional_tpms_pressure_rr.tpms_pressure_rr;
            if (std::isfinite(pressure) && pressure >= 0.0f) {
                publish_sensor("tpms_rear_right", pressure);
            }
        }
    }
}

void VehicleStateManager::set_asleep(bool asleep) {
    publish_binary_sensor("asleep", asleep);
}

void VehicleStateManager::set_charging(bool charging) {
    publish_binary_sensor("charging", charging);
}

void VehicleStateManager::set_parking_brake(bool engaged) {
    publish_binary_sensor("parking_brake", engaged);
}

void VehicleStateManager::set_door_state(const std::string& door_id, bool open) {
    publish_binary_sensor(door_id, open);
}

void VehicleStateManager::set_window_state(const std::string& window_id, bool open) {
    publish_binary_sensor(window_id, open);
}

void VehicleStateManager::set_battery_level(float level) {
    if (level >= 0.0f && level <= 100.0f && std::isfinite(level)) {
        publish_sensor("battery_level", level);
    }
}

}  // namespace tesla_ble_vehicle
}  // namespace esphome
