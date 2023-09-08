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
from pyorbbecsdk import *
import cv2

ESC = 27


def main():
    pipeline = Pipeline()
    assert pipeline is not None
    device = pipeline.get_device()
    assert device is not None
    if not device.is_property_supported(OBPropertyID.OB_STRUCT_CURRENT_DEPTH_ALG_MODE,
                                        OBPermissionType.PERMISSION_READ_WRITE):
        print("Current device not support depth work mode!")
        return
    current_depth_work_mode = device.get_depth_work_mode()
    assert current_depth_work_mode is not None
    print("Current depth work mode: ", current_depth_work_mode)
    depth_work_mode_list = device.get_depth_work_mode_list()
    assert depth_work_mode_list is not None
    for i in range(depth_work_mode_list.get_count()):
        depth_work_mode = depth_work_mode_list.get_depth_work_mode_by_index(i)
        assert depth_work_mode is not None
        print("{}. {}".format(i, depth_work_mode))
    if depth_work_mode_list.get_count() > 1:
        index = int(input("Please input depth work mode index: "))
        if depth_work_mode_list.get_count() > index >= 0:
            select_depth_work_mode = depth_work_mode_list.get_depth_work_mode_by_index(index)
            assert select_depth_work_mode is not None
            device.set_depth_work_mode(select_depth_work_mode)
            assert select_depth_work_mode == device.get_depth_work_mode()
            device.set_depth_work_mode(current_depth_work_mode)
            assert current_depth_work_mode == device.get_depth_work_mode()
            print("Set depth work mode to {} success!".format(select_depth_work_mode))
    device.set_depth_work_mode(current_depth_work_mode)


if __name__ == '__main__':
    main()
