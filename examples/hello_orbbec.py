# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.  
#  You may obtain a copy of the License at
#  
#      http:# www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
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
