

# 简介

包括esp32系列和树莓派pico系列。我将使用esp32-c6和rpi pico & rpi pico2-w dev-kit，但是，通常同一制造商的其他产品也可以使用。


# MicroPython

- [MicroPython](https://micropython.org/)

## esp32

- esp32
- esp32-s2
- esp32-s3
- esp32-c2
- eps32-c3
- esp32-c5
- esp32-c6
- esp32-c61
- esp32-h2
- esp32-p4

esp32, esp32-s系列是xtensa内核，esp32-c系列是risc-v内核，h2、p4也是risc-v。


## rpi-pico

- pico
- pico-w
- pico2
- pico2w

带w就是有无线模组(wifi、bt)，不带就没有无线模组，pico1是双核arm cortex-m0+，pico2是双核arm cortex-m3 + 双核risc-v，共4个cpu核，但m3和risc-v好像不能同时使用，只能切换使用。


# 安装MicroPython

## esp32

以ESP32-C6为例，去MicroPython官网下载固件：

- 主页: [esp32-c6](https://micropython.org/download/ESP32_GENERIC_C6/) ;
- 固件: [ESP32_GENERIC_C6-20250415-v1.25.0.bin](https://micropython.org/resources/firmware/ESP32_GENERIC_C6-20250415-v1.25.0.bin) ;
- EspTool : [flash download tool](https://dl.espressif.com/public/flash_download_tool.zip) ;

下载固件 `ESP32_GENERIC_C6-20250415-v1.25.0.bin`, 然后使用espressif官方的`flash download tool`或者Thonny下载固件到esp32-c6即可使用.


## rpi-pico

以树莓派pico2-w为例，去MicroPython官网下载固件：

- 主页: [pico2-w](https://micropython.org/download/RPI_PICO2_W/) ;
- 固件: [RPI_PICO2_W-20250415-v1.25.0.uf2](https://micropython.org/resources/firmware/RPI_PICO2_W-20250415-v1.25.0.uf2) ;

把树莓派pico2-w以大容量设备的方式插入电脑(按boot键同时插入电脑), 直接复制 `RPI_PICO2_W-20250415-v1.25.0.uf2` 到 pico2-w 的存储空间中即可使用.


# 集成开发环境

- Thonny
- VS Code
- Pycharm

Thonny可以直接把python代码刷到esp32和树莓派中，但是代码编辑功能没vs code和pycharm好用，可以使用后两者写代码，用thonny刷机。


# 源代码

- [esp32](esp32/README.md)
- [rpi-pico](rpi-pico/README.md)


# 扩展

- MicroPython
- CircuitePython
- PyMite
- Zerynth
- emPython
- Ripple
- Transcrypt
- QuecPython
- Pycopy
- OpenMV
- Loboris Micropython

上述很多都是MicroPython的分支，但都有一定特色。


# 模拟器

- [wokwi](https://wokwi.com/)
- [Renode](https://renode.io/)
- [esp32 qemu](https://github.com/espressif/qemu)
- [ESP-IDF Simulator](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/tools/qemu.html)
- [Proteus](https://www.labcenter.com/)
- [Simulink](https://www.mathworks.com/)
- [TinyGo](https://tinygo.org/)
- [PlatformIO](https://platformio.org/)

线上的，线下的，收费的，免费的都有，用模拟器做早期验证比较方便。


# License

MIT License.
