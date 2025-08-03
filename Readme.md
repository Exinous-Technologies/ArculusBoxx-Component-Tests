**ArculusBoxx Component Test Suite**

A comprehensive test harness for the ArculusBoxx embedded system, covering camera and I²C interfaces. This suite ensures that the hardware interfaces are correctly configured and that the Python-based test runner executes reliably in a controlled environment.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Python Virtual Environment](#python-virtual-environment)
4. [Running the Test Suite](#running-the-test-suite)

---

## Prerequisites

* A Raspberry Pi with camera and I²C interfaces available
* Python 3.9 or newer
* `sudo` privileges to install system packages and access hardware interfaces

---

## Initial Setup

Before creating the Python virtual environment, complete the following steps to enable the required hardware interfaces and install system dependencies.

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
