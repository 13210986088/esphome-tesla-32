#include "tesla_ble_vehicle_sensor.h"
#include "esphome/core/log.h"
#include "esphome/core/application.h"
#include "esphome/components/tesla_ble_vehicle/tesla_ble_vehicle.h"
#include "esphome/components/tesla_ble_vehicle/vehicle_state_manager.h"

namespace esphome {
namespace tesla_ble_vehicle {

static const char *TAG = "tesla_ble_vehicle.sensor";

void TeslaBLEVehicleSensor::setup() {
  ESP_LOGCONFIG(TAG, "Tesla BLE Vehicle Sensor component setup.");
}

void TeslaBLEVehicleSensor::update() {
  ESP_LOGD(TAG, "Updating vehicle data...");

  auto *vehicle = App.get_component<TeslaBLEVehicle>();
  if (vehicle == nullptr) {
    ESP_LOGW(TAG, "TeslaBLEVehicle component not found.");
    return;
  }

  if (!vehicle->is_connected()) {
    ESP_LOGW(TAG, "Vehicle not connected.");
    return;
  }

  VehicleStateManager *state = vehicle->get_state_manager();
  if (state == nullptr) {
    ESP_LOGW(TAG, "VehicleStateManager is null.");
    return;
  }

  // 辅助 lambda：从内部传感器读取状态并发布
  auto publish_from_internal = [&](sensor::Sensor *target, const std::string &internal_id) {
    if (target == nullptr) return;
    auto *internal = state->get_sensor(internal_id);
    if (internal != nullptr && internal->has_state()) {
      target->publish_state(internal->state);
      ESP_LOGD(TAG, "Published %s: %.2f", internal_id.c_str(), internal->state);
    } else {
      ESP_LOGW(TAG, "Internal sensor '%s' not available.", internal_id.c_str());
    }
  };

  // 批量搬运所有可能的传感器
  publish_from_internal(battery_level_sensor_,       "battery_level");
  publish_from_internal(range_sensor_,               "range");
  publish_from_internal(range_rated_api_sensor_,     "range_rated_api");
  publish_from_internal(outside_temp_sensor_,        "outside_temp");
  publish_from_internal(inside_temp_sensor_,         "inside_temp");
  publish_from_internal(driver_temp_setting_sensor_, "driver_temp_setting");
  publish_from_internal(passenger_temp_setting_sensor_,"passenger_temp_setting");
  publish_from_internal(speed_sensor_,               "speed");
  publish_from_internal(odometer_sensor_,            "odometer");
  publish_from_internal(charger_power_sensor_,       "charger_power");
  publish_from_internal(charger_voltage_sensor_,     "charger_voltage");
  publish_from_internal(charger_current_sensor_,     "charger_current");
  publish_from_internal(charging_rate_sensor_,       "charging_rate");
  publish_from_internal(charge_rate_sensor_,         "charge_rate");
  publish_from_internal(energy_added_sensor_,        "energy_added");
  publish_from_internal(charge_energy_added_sensor_, "charge_energy_added");
  publish_from_internal(time_to_full_sensor_,        "time_to_full");
  publish_from_internal(time_to_full_charge_sensor_, "time_to_full_charge");
  publish_from_internal(tpms_fl_sensor_,             "tpms_front_left");
  publish_from_internal(tpms_fr_sensor_,             "tpms_front_right");
  publish_from_internal(tpms_rl_sensor_,             "tpms_rear_left");
  publish_from_internal(tpms_rr_sensor_,             "tpms_rear_right");
}

}  // namespace tesla_ble_vehicle
}  // namespace esphome
