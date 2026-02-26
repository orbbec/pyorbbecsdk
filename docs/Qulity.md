pyorbbecsdk SDK 质量提升与自动化测试计划
Context
当前 pyorbbecsdk 存在以下问题：

测试框架为 unittest，无 pytest 配置，无 conftest.py，无 fixture 共享，无 skip 机制
4个测试文件全部强依赖硬件，无设备则直接 crash（assertGreater(device_list.get_count(), 0)）
测试覆盖盲区：无帧数据验证、无滤镜测试、无性能基准、无错误恢复测试
无自动化测试报告生成，无 CI 测试流程
示例代码使用 from pyorbbecsdk import *（wildcard），无 docstring，用 print 代替 logging
初级开发者缺乏引导：无分步快速上手文档，错误信息不友好
总体方案（分三大模块）
## 模块一：测试基础设施重构
1.1 迁移到 pytest + 创建 conftest.py
新建文件：test/conftest.py

包含：

@pytest.fixture(scope="session") 的 device fixture：连接摄像头，全局复用
@pytest.fixture(scope="session") 的 pipeline fixture
@pytest.mark.hardware marker：标记需要实际硬件的测试
pytest_configure 函数：注册 hardware marker
全局 skip_if_no_device fixture：自动跳过（不崩溃）
Gemini 335 专用 gemini335_device fixture：验证设备型号

# 核心结构
@pytest.fixture(scope="session")
def device():
    ctx = Context()
    device_list = ctx.query_devices()
    if device_list.get_count() == 0:
        pytest.skip("No Orbbec device connected")
    return device_list.get_device_by_index(0)
修改文件：pyproject.toml

添加 pytest 配置节：


[tool.pytest.ini_options]
testpaths = ["test"]
markers = ["hardware: requires physical camera", "gemini335: Gemini 335 specific"]
addopts = "--html=reports/test_report.html --self-contained-html -v"
新建文件：test/requirements_test.txt


pytest>=7.4.0
pytest-html>=4.0.0
pytest-timeout>=2.2.0
pytest-xdist>=3.3.0  # 并行测试
numpy
opencv-python
### 1.2 重构现有测试文件
修改文件：test/test_context.py、test/test_device.py、test/test_pipeline.py、test/test_sensor_control.py

改造要点：

继承 pytest 风格（保留 class，改用 fixture 注入 device）
用 pytest.mark.hardware 标记所有硬件测试
将 return early if not supported 改为 pytest.skip(reason=...)
消除 test_pipeline.py 和 test_device.py 中的重复 test_get_device_info
模块二：Gemini 335 专项自动化测试套件
## 2.1 设备发现与基础信息测试
新建文件：test/test_gemini335_device.py

测试用例：

test_device_discovery - 验证设备可被枚举，name 包含 "Gemini 335"
test_device_info_completeness - 验证 PID/VID/序列号/固件版本/硬件版本非空
test_firmware_version_format - 验证固件版本格式（如 1.2.34）
test_device_temperature_range - 温度在合理范围（0-80°C）
test_connection_type - 验证 USB 连接类型
test_sensor_list - 验证 Depth/Color/IR sensor 存在
## 2.2 流数据测试
新建文件：test/test_gemini335_streams.py

深度流测试
test_depth_stream_starts - 深度流可以正常启动
test_depth_frame_dimensions - 验证帧宽高与配置匹配（640×480、848×480 等）
test_depth_frame_data_nonzero - 深度帧中有效像素 > 10%（不全黑）
test_depth_scale_factor - depth_scale 在合理范围（0.0001 ~ 0.01）
test_depth_range_validity - 有效深度值在 20mm ~ 10000mm 内
test_depth_timestamp_monotonic - 连续 30 帧时间戳单调递增
test_depth_fps_accuracy - 30fps 配置下实测帧率在 28-32fps 内
彩色流测试
test_color_stream_starts - 彩色流可以正常启动
test_color_frame_dimensions - 帧尺寸与配置匹配
test_color_frame_not_black - 图像均值 > 5（不全黑）
test_color_formats - RGB、BGR、MJPEG 格式均可切换
test_color_timestamp_monotonic - 时间戳单调递增
IR 流测试
test_ir_stream_starts - IR 流可以正常启动
test_ir_frame_data_valid - IR 帧有有效数据
多流同步测试
test_color_depth_sync - 彩色+深度同时流，时间戳差 < 33ms（1帧误差）
test_frame_sync_enabled - 开启 frame sync 后时间戳差 < 10ms
test_multi_stream_pipeline - 同时启动 3 路流（Color/Depth/IR），连续采集 60 帧无丢帧
2.3 传感器控制测试
新建文件：test/test_gemini335_controls.py

模板（每个控制项）：


def test_depth_exposure_set_get(device):
    # 1. 关闭自动曝光
    # 2. 记录当前值
    # 3. 设置新值（当前值+合法偏移）
    # 4. 读回，断言与设置值一致
    # 5. 恢复原始值
    # 6. 断言恢复成功
覆盖控制项：

深度曝光/增益（手动/自动模式）
彩色曝光/增益/白平衡（手动/自动模式）
IR 曝光/增益（手动/自动模式）
激光强度（LDP/Laser/Flood）
镜像和翻转（Depth/Color/IR 三轴）
软件滤波器开关
## 2.4 滤镜管线测试
新建文件：test/test_gemini335_filters.py

test_temporal_filter - 时序滤波后深度帧噪声（stddev）降低 > 10%
test_spatial_filter - 空间滤波后空洞减少（零值像素减少）
test_hole_filling_filter - HoleFillingFilter 后 NaN/0 比例降低
test_decimation_filter - DecimationFilter 正确缩减分辨率（2×=50%面积）
test_threshold_filter - ThresholdFilter 截断后超范围值为 0
test_align_filter - AlignFilter 输出 color 分辨率的深度图
test_point_cloud_filter - PointCloudFilter 输出点数 > 0，坐标范围合理
## 2.5 相机内参与标定测试
新建文件：test/test_gemini335_calib.py

test_camera_intrinsics - 获取深度/彩色内参（fx/fy/cx/cy/w/h）非零
test_depth_intrinsics_range - fx/fy 在 100-2000 范围内（物理合理性）
test_color_intrinsics_range - 同上
test_extrinsic_rotation_identity - 旋转矩阵行列式 ≈ 1（正交矩阵）
test_calibration_params_list - 获取所有标定组，count > 0
## 2.6 性能基准测试
新建文件：test/test_gemini335_performance.py

test_depth_stream_latency - 第一帧到达时间 < 3s
test_depth_fps_stability_60s - 60秒内深度流帧率标准差 < 1fps（稳定性）
test_color_depth_sync_latency - 双流同步延迟 < 33ms（P95）
test_pipeline_restart_time - stop→start 重启时间 < 2s
test_frame_processing_throughput - numpy 帧处理（resize+normalize）跟得上 30fps
模块三：自动化报告与开发者体验
## 3.1 自动化测试报告
新建目录：reports/（git ignore 报告内容，保留模板）

新建文件：test/generate_report.py

功能：

调用 pytest，生成 HTML 报告（使用 pytest-html）
自动在报告头部注入：
测试日期/SDK版本
设备信息（型号、固件、序列号）
测试环境（OS、Python版本）
报告按模块分组展示通过/失败/跳过统计

# 核心调用
import pytest
import sys

def generate_report(device_info: dict, version: str):
    report_path = f"reports/test_report_{version}_{date}.html"
    args = [
        "test/",
        f"--html={report_path}",
        "--self-contained-html",
        "-v",
        "--timeout=30",    # 每个测试超时
        f"--metadata=SDK版本={version}",
        f"--metadata=设备={device_info['name']}",
    ]
    return pytest.main(args)
新建文件：.github/workflows/test.yml（CI 自动化）


# 在 self-hosted runner 连接 Gemini 335 的机器上运行
on: [push, pull_request, workflow_dispatch]
jobs:
  hardware-test:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - name: Run tests and generate report
        run: python test/generate_report.py
      - uses: actions/upload-artifact@v4
        with:
          name: test-report
          path: reports/*.html
3.2 初级开发者体验提升
新建文件：examples/beginner/01_hello_camera.py

特点：

每一步都有注释，解释为什么这样做
友好的错误提示（"未找到设备，请检查USB连接"，而非 crash）
使用 try/finally 保证资源释放
展示如何查看当前帧的元数据
新建文件：examples/beginner/02_depth_visualization.py

逐步构建：原始深度图 → 归一化 → 彩色映射 → 距离标注
新建文件：examples/beginner/03_color_and_depth_aligned.py

讲解对齐的概念，演示 AlignFilter
## 3.3 高级开发者体验提升
新建文件：examples/advanced/high_performance_pipeline.py

演示多线程回调+帧队列，避免 wait_for_frames 阻塞
性能测量（帧率计数器、处理延迟）
帧丢弃策略
新建文件：examples/advanced/custom_filter_chain.py

展示滤镜链组合方式（Temporal→Spatial→HoleFilling→Align→PointCloud）
每步滤镜效果对比
关键文件清单
文件路径	操作	说明
test/conftest.py	新建	pytest fixtures，device/pipeline/skip_if_no_device
test/test_gemini335_device.py	新建	设备基础信息测试
test/test_gemini335_streams.py	新建	Depth/Color/IR 流数据验证
test/test_gemini335_controls.py	新建	传感器控制参数读写测试
test/test_gemini335_filters.py	新建	滤镜管线功能测试
test/test_gemini335_calib.py	新建	相机内外参标定测试
test/test_gemini335_performance.py	新建	性能基准测试
test/generate_report.py	新建	自动化报告生成脚本
test/requirements_test.txt	新建	测试专用依赖
pyproject.toml	修改	添加 pytest 配置节
test/test_context.py	修改	改为 pytest 风格，添加 skip
test/test_device.py	修改	改为 pytest 风格，添加 skip
test/test_pipeline.py	修改	改为 pytest 风格，去重
test/test_sensor_control.py	修改	改为 pytest 风格，skip 替代 return
examples/beginner/01_hello_camera.py	新建	初级快速上手
examples/beginner/02_depth_visualization.py	新建	深度可视化
examples/advanced/high_performance_pipeline.py	新建	高性能管线示例
.github/workflows/test.yml	新建	CI 自动化测试
可复用的现有代码
examples/utils.py 中的 frame_to_bgr_image()：彩色帧转换
test/test_sensor_control.py 中的 turn_off_depth_auto_exposure() 等辅助方法：迁移到 conftest.py 作为 fixture
所有示例中的 try: ... except OBError 错误处理模式
pipeline.py 中的 enable_frame_sync() 和 wait_for_frames() 模式
实施顺序
先建 conftest.py 和测试依赖（基础设施，其他测试依赖它）
安装测试依赖 pip install -r test/requirements_test.txt
建 test_gemini335_device.py（最基础，验证连接）
建 test_gemini335_streams.py（核心功能验证）
建 test_gemini335_controls.py（传感器控制）
建 test_gemini335_filters.py（滤镜管线）
建 test_gemini335_calib.py（标定参数）
建 test_gemini335_performance.py（性能基准）
修改 pyproject.toml，添加 pytest 配置
建 generate_report.py，运行完整报告
重构现有 4 个测试文件到 pytest 风格
新建初级/高级示例
验证方式

# 安装依赖
pip install -r test/requirements_test.txt

# 运行所有 Gemini 335 测试（确保摄像头已连接）
pytest test/test_gemini335_*.py -v

# 跳过硬件测试（无摄像头环境）
pytest test/ -v -m "not hardware"

# 生成 HTML 报告
python test/generate_report.py

# 查看报告
start reports/test_report_*.html
生成的 HTML 报告包含：每个测试模块的通过率、耗时、Gemini 335 设备元数据、失败详情（含截图如适用）。