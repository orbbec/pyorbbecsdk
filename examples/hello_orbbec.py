from pyorbbecsdk import get_version, get_stage_version
from pyorbbecsdk import Context


def main():
    print("Hello Orbbec!")
    print("SDK version: {}".format(get_version()))
    print("SDK stage version: {}".format(get_stage_version()))
    context = Context()
    device_list = context.query_devices()
    if device_list.get_count() == 0:
        print("No device connected")
        return
    device = device_list.get_device_by_index(0)
    device_info = device.get_device_info()
    print("Device info: {}".format(device_info))
    print("Sensor list:")
    sensor_list = device.get_sensor_list()
    for i in range(sensor_list.get_count()):
        sensor = sensor_list.get_sensor_by_index(i)
        print("  {}".format(sensor.get_type()))


if __name__ == "__main__":
    main()
