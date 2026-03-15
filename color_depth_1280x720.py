import cv2
import numpy as np
from pyorbbecsdk import Pipeline, Config, OBError, OBSensorType, OBFormat

def main():
    # 1. 创建管道实例
    pipeline = Pipeline()
    
    # 2. 创建配置对象
    config = Config()
    
    # 目标分辨率
    TARGET_WIDTH = 1280
    TARGET_HEIGHT = 720
    
    try:
        # 3. 获取设备以查询支持的流配置
        device = pipeline.get_device()
        if device is None:
            print("未检测到设备！")
            return
        
        # 4. 配置彩色流 (寻找最接近 1280x720 的配置)
        color_sensor = device.get_sensor(OBSensorType.COLOR_SENSOR)
        if color_sensor:
            color_profiles = color_sensor.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            selected_color_profile = None
            
            # 优先查找精确匹配 1280x720 的配置
            for profile in color_profiles:
                if profile.get_width() == TARGET_WIDTH and profile.get_height() == TARGET_HEIGHT:
                    selected_color_profile = profile
                    print(f"找到精确匹配的彩色流配置: {TARGET_WIDTH}x{TARGET_HEIGHT}@{profile.get_fps()}fps")
                    break
            
            # 如果没有精确匹配，查找最接近的
            if not selected_color_profile:
                print(f"未找到精确匹配的 {TARGET_WIDTH}x{TARGET_HEIGHT} 彩色流配置，使用默认配置。")
                config.enable_stream(OBSensorType.COLOR_SENSOR)
            else:
                config.enable_stream(selected_color_profile)
        else:
            print("未找到彩色传感器，使用默认配置。")
            config.enable_stream(OBSensorType.COLOR_SENSOR)
        
        # 5. 配置深度流 (寻找最接近 1280x720 的配置)
        depth_sensor = device.get_sensor(OBSensorType.DEPTH_SENSOR)
        if depth_sensor:
            depth_profiles = depth_sensor.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            selected_depth_profile = None
            
            # 优先查找精确匹配 1280x720 的配置
            for profile in depth_profiles:
                if profile.get_width() == TARGET_WIDTH and profile.get_height() == TARGET_HEIGHT:
                    selected_depth_profile = profile
                    print(f"找到精确匹配的深度流配置: {TARGET_WIDTH}x{TARGET_HEIGHT}@{profile.get_fps()}fps")
                    break
            
            # 如果没有精确匹配，查找最接近的
            if not selected_depth_profile:
                print(f"未找到精确匹配的 {TARGET_WIDTH}x{TARGET_HEIGHT} 深度流配置，使用默认配置。")
                config.enable_stream(OBSensorType.DEPTH_SENSOR)
            else:
                config.enable_stream(selected_depth_profile)
        else:
            print("未找到深度传感器，使用默认配置。")
            config.enable_stream(OBSensorType.DEPTH_SENSOR)
        
        # 6. 启动管道
        print("\n正在启动管道...")
        pipeline.start(config)
        print("管道启动成功，按 'q' 键退出程序。")
        
        while True:
            # 7. 等待帧数据 (超时时间 1000ms)
            frames = pipeline.wait_for_frames(1000)
            if frames is None:
                continue
            
            # 8. 获取彩色帧和深度帧
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            
            if color_frame is None or depth_frame is None:
                continue
            
            # 9. 处理彩色图像
            color_data = np.ascontiguousarray(color_frame.get_data())
            color_format = color_frame.get_format()
            
            if color_format == OBFormat.MJPG:
                color_image = cv2.imdecode(color_data, cv2.IMREAD_COLOR)
            elif color_format == OBFormat.RGB:
                color_image = cv2.cvtColor(color_data, cv2.COLOR_RGB2BGR)
            elif color_format == OBFormat.BGR:
                color_image = color_data
            else:
                color_image = color_data
            
            # 10. 处理深度图像
            depth_data = np.ascontiguousarray(depth_frame.get_data())
            depth_format = depth_frame.get_format()
            
            if depth_format == OBFormat.Y16:
                depth_image = depth_data.view(np.uint16).reshape(depth_frame.get_height(), depth_frame.get_width())
            else:
                depth_image = depth_data
            
            # 将深度图转换为可视化的彩色图
            depth_vis = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
            
            # 11. 显示图像和分辨率信息
            cv2.putText(color_image, f"Color: {color_frame.get_width()}x{color_frame.get_height()}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(depth_vis, f"Depth: {depth_frame.get_width()}x{depth_frame.get_height()}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # 显示中心点深度值
            h, w = depth_image.shape
            center_depth = depth_image[h//2, w//2]
            if center_depth > 0:
                cv2.putText(depth_vis, f"Center Depth: {center_depth} mm", 
                            (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Orbbec Color Stream", color_image)
            cv2.imshow("Orbbec Depth Stream", depth_vis)
            
            # 12. 按键检测
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
                
    except OBError as e:
        print(f"发生错误: {e}")
    except KeyboardInterrupt:
        print("\n用户中断程序")
    finally:
        # 13. 清理资源
        print("正在停止管道...")
        pipeline.stop()
        cv2.destroyAllWindows()
        print("程序已退出。")

if __name__ == "__main__":
    main()
