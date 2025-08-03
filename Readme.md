# **ArculusBoxx Component Test Suite**

A comprehensive test harness for the ArculusBoxx embedded system, covering camera and I²C interfaces. This suite ensures that the hardware interfaces are correctly configured and that the Python-based test runner executes reliably in a controlled environment.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Python Virtual Environment](#python-virtual-environment)
4. [Running the Test Suite](#running-the-test-suite)
5. [Main Application](#main-application)
6. [Module Overview](#module-overview)

---

## Prerequisites

* A Raspberry Pi with camera and I²C interfaces available
* Python 3.9 or newer
* `sudo` privileges to install system packages and access hardware interfaces

---

## Initial Setup

Before creating the Python virtual environment, complete the following steps to enable the required hardware interfaces, install system dependencies, and configure optional UPS HAT (D) battery monitoring.

### 1. Enable Interfaces

Run `raspi-config` to enable the camera and I²C support:

```bash
sudo raspi-config
```

Navigate to:

* **Interface Options > Camera** > Enable
* **Interface Options > I2C** > Enable

Exit `raspi-config` when done.

### 2. Install System Packages

Update the package list and install the required libraries:

```bash
sudo apt update
sudo apt install -y libcamera-dev libcamera-apps libcap-dev
```

These packages provide access to the Raspberry Pi camera subsystem and allow privilege elevations for camera apps.

### 3. UPS HAT (D) Battery Level Display Setup

If you're using the Waveshare UPS HAT (D) for battery monitoring, follow these steps to enable the battery level display:

```bash
sudo apt-get install p7zip
wget https://files.waveshare.com/wiki/UPS-HAT-D/UPS_HAT_D.7z
7zr x UPS_HAT_D.7z -r -o./
cd UPS_HAT_D
./main.sh   #Do not add 'sudo'
sudo reboot
```

After rebooting, you should see a battery icon in the upper right corner of your desktop. This indicates that the UPS HAT (D) battery monitoring is working correctly. The battery icon will display information about battery capacity, voltage, and remaining charge when you hover over it.

**Note:** If the battery level drops below 5%, a low battery warning will appear, and the system will automatically power off after 60 seconds if no charging power is connected.

---

## Python Virtual Environment

Isolate Python dependencies using a virtual environment.

1. Ensure you have Python 3.9 or greater:

   ```bash
   python3 --version
   ```
2. Create and activate the virtual environment (allow system-site packages if needed):

   ```bash
   python3 -m venv --system-site-packages venv
   source venv/bin/activate
   ```
3. Install Python dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Running the Test Suite

Execute the main test runner with preserved environment variables:

```bash
sudo --preserve-env=VIRTUAL_ENV,PATH python main.py
```

**Note:** `sudo` is required to access the camera and I²C hardware devices. The `--preserve-env` flags ensure the virtual environment is used.

---

## Main Application

The `main.py` file serves as the central test runner for the ArculusBoxx system. It provides an interactive menu-driven interface that allows you to test individual hardware components or run comprehensive system tests.

### Features

- **Interactive Menu System**: Choose from 9 different test options
- **Hardware Component Testing**: Test individual sensors, actuators, and interfaces
- **Flexible Endstop Testing**: Supports testing two endstop switches in any order
- **Camera Testing**: Tests both outer and inner cameras with image capture
- **Real-time Feedback**: Provides immediate feedback on test results

### Test Options

1. **NeoPixel Startup Test**: Runs a color wave sequence on the LED strip
2. **Weight Reading Test**: Reads weight measurements from load cells
3. **Relay Test**: Tests relay modules (Left Lock, Right Lock, Buzzer)
4. **RFID Module Test**: Tests RFID card reading functionality
5. **PIR Sensor Test**: Tests motion detection with PIR sensor
6. **Endstop Switch Test**: Tests mechanical endstop switches
7. **Outer Camera Test**: Tests external camera with image capture
8. **Inner Camera Test**: Tests internal camera using PiCamera2
9. **QR Code Scan Test**: Tests QR code scanning functionality

### Usage

When you run `main.py`, you'll be presented with a numbered menu. Simply enter the number corresponding to the test you want to run. The application will guide you through each test with clear instructions and feedback.

---

## Module Overview

The test suite is organized into specialized modules, each handling specific hardware components:

### Core Hardware Modules

- **`led.py`**: NeoPixel LED strip control with startup test sequences
- **`load_cells.py`**: HX711 load cell amplifier interface for weight measurements
- **`relay.py`**: Single-channel relay control with context management
- **`endstop.py`**: Mechanical endstop switch testing with press/release detection

### Sensor Modules

- **`pir_sensor.py`**: PIR motion sensor testing with calibration and motion detection
- **`rfid.py`**: MFRC522 RFID reader interface for card detection
- **`qr_reader.py`**: Serial-based QR code scanner interface

### Camera Modules

- **`camera.py`**: Multi-camera testing framework with OpenCV integration
- **`picamera.py`**: PiCamera2 interface for Raspberry Pi camera testing

### Test Utilities

- **`loadcell_callibrate.py`**: Load cell calibration utility

Each module provides both standalone functionality and integration with the main test runner, allowing for both individual component testing and comprehensive system validation.

---
