
[English](OrbbecSDKConfig.md) | **中文**

<a id="orbbec-sdk-configuration-file-introduction-orbbecsdkconfig_v10xml"></a>

# Orbbec SDK 配置文件介绍（OrbbecSDKConfig_v1.0.xml）

Orbbec SDK 配置文件是用于定义 SDK 全局配置的 XML 文件。

初始化时，SDK Context 会加载配置文件并将其应用为全局配置。如果使用自定义配置文件，可在调用 Context 构造函数时传入文件路径。如果未提供路径或传入空字符串，SDK 会在工作目录中查找 `OrbbecSDKConfig.xml`。如果指定文件和默认文件都不存在，SDK 将使用内置默认配置。

<a id="log-configuration"></a>

## 日志配置

日志配置主要包括全局日志级别、控制台和文件输出级别、日志保存路径、单个日志文件大小以及日志文件数量。

```cpp
    <Log>
        <!--Log output level, int type, optional values: 0-DEBUG, 1-INFO, 2-WARN, 3-ERROR, 4-FATAL, 5-OFF-->
        <!--Log level configuration execution priority: 0. Application code configuration > 1. Detailed configuration of configuration file (file & console configuration) > 2. Global configuration of configuration file > 3. SDK code default configuration (file: 0, terminal: 1)-->
        <!--Global log output level-->
        <LogLevel>0</LogLevel>
        <!--File log output level-->
        <FileLogLevel>0</FileLogLevel>
        <!--Console log output level-->
        <ConsoleLogLevel>1</ConsoleLogLevel>
        <!--Default log output file path, string type. If this item is not configured, the default path will be used: Win/Linux: "./Log"; Android: "/sdcard/3DCamera/Log"-->
        <!--<OutputDir>./log</OutputDir>-->
        <!--Default log output file size, int type, unit: MB-->
        <MaxFileSize>100</MaxFileSize>
        <!--Default log output file number (circular overwrite), int type-->
        <MaxFileNum>3</MaxFileNum>
        <!--Log asynchronous output, changing to asynchronous output can reduce the blocking time of printing logs, but some logs may be lost when the program exits abnormally; true-enable, false-disable (default)-->
        <Async>false</Async>
    </Log>
```

<a id="memory-configuration"></a>

## 内存配置

```cpp
    <Memory>
        <!--Enable memory pool to reuse frame memory, avoid frequent memory allocation and release. true-enable, false-disable)-->
        <EnableMemoryPool> true </EnableMemoryPool>
        <!--Maximum memory size of all data frames, int type, unit: MB, minimum 100MB-->
        <MaxFrameBufferSize> 2048 </MaxFrameBufferSize>
        <!--Frame buffer queue size in pipeline-->
        <PipelineFrameQueueSize>10</PipelineFrameQueueSize>
        <!--Frame buffer queue size in internal processing unit-->
        <FrameProcessingBlockQueueSize>10</FrameProcessingBlockQueueSize>
    </Memory>
```

**说明**

1. 内存池默认大小为 2GB（2048MB）。

```cpp
        <MaxFrameBufferSize> 2048 </MaxFrameBufferSize>
```

2. Pipeline 的帧缓冲队列默认长度为 10。主机处理较慢时，SDK 内部最多缓存 10 帧，可能增加用户获取帧的延迟。如果延迟明显，可减少缓冲数量。

```cpp
        <PipelineFrameQueueSize>10</PipelineFrameQueueSize>
```

3. 内部处理单元的队列默认长度为 10。主机处理较慢时，SDK 内部最多缓存 10 帧，可能增加用户获取帧的延迟。如果延迟明显，可减少队列长度。

```cpp
        <FrameProcessingBlockQueueSize>10</FrameProcessingBlockQueueSize>
```

<a id="global-timestamp"></a>

## 全局时间戳

基于设备时间戳并考虑数据传输延迟，通过线性回归将其映射到系统时间戳，可用于同步多个不同设备的时间戳。实现流程如下：

1. 全局时间戳拟合器：定期获取设备时间戳与当前系统时间戳，通过线性回归计算拟合方程参数。
2. 全局时间戳转换器：将数据帧时间戳转换为与设备时间戳相同的单位，再根据设备时间戳计算溢出次数并转换为 64 位时间戳，最后根据拟合器输出的参数转换为全局时间戳。

```cpp
    <Misc>
        <GlobalTimestampFitterEnable>true</GlobalTimestampFitterEnable>
        <!--Global timestamp fitter refresh interval, unit: milliseconds, default value: 1000, minimum value: 100, it is recommended not to be greater than 1000 -->
        <GlobalTimestampFitterInterval>1000</GlobalTimestampFitterInterval>
        <!--Global timestamp fitter queue size, default value: 100, minimum value: 20 -->
        <GlobalTimestampFitterQueueSize>100</GlobalTimestampFitterQueueSize>
    </Misc>
```

1. 原文说明默认每八秒获取设备时间以更新全局时间戳拟合器；下方配置示例为 1000 ms。实际值请以所用 SDK 配置为准。

```cpp
        <GlobalTimestampFitterInterval>1000</GlobalTimestampFitterInterval>
```

2. 原文说明全局时间戳拟合器的默认队列长度为 10；下方配置示例为 100。实际值请以所用 SDK 配置为准。

```cpp
        <GlobalTimestampFitterQueueSize>100</GlobalTimestampFitterQueueSize>
```

**说明**

1. 全局时间戳主要支持 Gemini 330 系列。也支持 Gemini 2、Gemini 2L、Femto Mega 和 Femto Bolt，但尚未充分测试。如果这些设备出现稳定性问题，可关闭全局时间戳功能。

```cpp
        <GlobalTimestampFitterEnable>false</GlobalTimestampFitterEnable>
```

<a id="pipeline-configuration"></a>

## Pipeline 配置

```cpp
    <!--Default working configuration of pipeline-->
    <Pipeline>
        <Stream>
            <Depth>
                <!--Use default stream profile, bool type, true: use default stream profile, false: use specified stream profile in the configuration file-->
                <UseDefaultStreamProfile>true</UseDefaultStreamProfile>
            </Depth>
            <Color>
                <UseDefaultStreamProfile>true</UseDefaultStreamProfile>
            </Color>
            <!--If you need to open other streams, you can refer to the above format to add configuration-->
        </Stream>
    </Pipeline>
```

1. Pipeline 主要配置启用哪些视频流，默认仅启用 Depth 和 Color。可按以下方式添加 IR、左 IR 和右 IR 流。

```cpp
<!--If you need to open other streams, you can refer to the above format to add configuration-->
            <IR>
                <UseDefaultStreamProfile>true</UseDefaultStreamProfile>
            </IR>
            <LeftIR>
                <UseDefaultStreamProfile>true</UseDefaultStreamProfile>
            </LeftIR>
            <RightIR>
                <UseDefaultStreamProfile>true</UseDefaultStreamProfile>
            </RightIR>
```

<a id="device-configuration"></a>

## 设备配置

```cpp
    <!--Default configuration of data streams for different types of devices-->
    <Device>
        <EnumerateNetDevice>true</EnumerateNetDevice>
        <!--UVC Backend select on Linux; optional values: Auto, V4L2, LibUVC; Auto is the default value-->
        <LinuxUVCBackend>LibUVC</LinuxUVCBackend>

            <!--Gemini 335 config-->
        <Gemini335>
	        <!--Whether to enable heartbeat by default-->
	        <DefaultHeartBeat>0</DefaultHeartBeat>

			<Depth>
			    <!--Number of retries for open stream failures, 0 means no retries-->
				<StreamFailedRetry>0</StreamFailedRetry>
				<!--Open flow waits for the timeout period of the first frame of data, after which the open flow will fail-->
				<MaxStartStreamDelayMs>5000</MaxStartStreamDelayMs>
				<!--The maximum frame interval time, if this value is exceeded, it will be judged that the stream is interrupted-->
				<MaxFrameIntervalMs>2000</MaxFrameIntervalMs>
                <!--The resolution width is enabled by default, int type-->
                <Width>848</Width>
                <!--High resolution is enabled by default, int type-->
                <Height>480</Height>
                <!--The frame rate of the resolution enabled by default, int type-->
                <FPS>30</FPS>
                <Format>Y16</Format>
            </Depth>
            <Color>
                <!--The resolution width is enabled by default, int type-->
                <Width>1280</Width>
                <!--High resolution is enabled by default, int type-->
                <Height>720</Height>
                <!--The frame rate of the resolution enabled by default, int type-->
                <FPS>30</FPS>
                <Format>MJPG</Format>
            </Color>
            <IR>
                <!--The resolution width is enabled by default, int type-->
                <Width>848</Width>
                <!--High resolution is enabled by default, int type-->
                <Height>480</Height>
                <!--The frame rate of the resolution enabled by default, int type-->
                <FPS>30</FPS>
                <Format>Y8</Format>
            </IR>
			<LeftIR>
                <!--The resolution width is enabled by default, int type-->
                <Width>848</Width>
                <!--High resolution is enabled by default, int type-->
                <Height>480</Height>
                <!--The frame rate of the resolution enabled by default, int type-->
                <FPS>30</FPS>
                <Format>Y8</Format>
            </LeftIR>
			<RightIR>
                <!--The resolution width is enabled by default, int type-->
                <Width>848</Width>
                <!--High resolution is enabled by default, int type-->
                <Height>480</Height>
                <!--The frame rate of the resolution enabled by default, int type-->
                <FPS>30</FPS>
                <Format>Y8</Format>
            </RightIR>
        </Gemini335>
    </Device>
```

1. 设置是否枚举网络设备。Femto Mega 和 Gemini 2 XL 支持网络功能；需要使用这两款设备的网络功能时，可设为 true。

```cpp
        <EnumerateNetDevice>true</EnumerateNetDevice>
```

2. 设置在 Linux 或 ARM 上使用 LibUVC 还是 V4L2 接收数据。并非所有设备均支持 V4L2，建议使用 LibUVC。Gemini 330 系列支持 V4L2，但获取 Metadata 数据需要内核补丁。

```cpp
        <LinuxUVCBackend>LibUVC</LinuxUVCBackend>
```

3. 设置分辨率、帧率和数据格式。
