# ModelScope Space Reproduction: Safety Helmet Detection

[![ModelScope](https://img.shields.io/badge/ModelScope-Space-blue)](https://modelscope.cn/)
[![Gradio](https://img.shields.io/badge/Gradio-6.2.0-orange)](https://www.gradio.app/)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)](./LICENSE)

[中文版 / Chinese Version](./README.md)

A deployable safety helmet detection demo adapted for **ModelScope Space**.  
This project uses **ModelScope + Gradio + OpenCV** to detect whether people in an image are wearing safety helmets and returns a visualized result image.

---

## Overview

This repository is a practical **ModelScope Space** demo built on the following model:

- Model: `damo/cv_tinynas_object-detection_damoyolo_safety-helmet`

Supported workflow:

1. Upload an image
2. Load the model and run detection
3. Draw bounding boxes, labels, and confidence scores
4. Return the processed image

This repository is suitable for:

- ModelScope Space deployment practice
- Safety helmet detection reproduction
- Gradio image detection demos
- Local debugging + cloud deployment workflow

---

## Badge Summary

- **ModelScope Space**: target deployment platform
- **Gradio 6.2.0**: interactive UI framework
- **Python 3.11**: recommended local runtime
- **Apache 2.0**: open-source license

---

## Demo Preview

![Demo Result](./assets/demo-result.png)

Suggested preview contents:

- detection result after uploading a test image
- bounding boxes, labels, and confidence rendering
- actual ModelScope Space running interface

---

## Environment Compatibility

This version is adapted for the following **ModelScope Space** environment:

- **SDK**: `gradio`
- **Gradio Version**: `6.2.0`
- **Image Version**: `ubuntu22.04-py311-torch2.9.1-modelscope1.35.0`
- **Cloud Resource**: Free CPU

---

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
└── README.en.md
```

File descriptions:

- `app.py`: main application file including model loading, inference, and Gradio UI
- `requirements.txt`: dependency list
- `README.md`: Chinese documentation
- `README.en.md`: English documentation

---

## Core Implementation

This project keeps the typical inference structure for safety helmet detection:

- `pipeline(Tasks.domain_specific_object_detection, model=...)`
- `OutputKeys.SCORES / LABELS / BOXES`
- `cv2.rectangle(...)`
- `cv2.putText(...)`

To improve stability for ModelScope Space and Gradio 6.2.0, this project uses a more robust implementation style and adopts:

- `opencv-python-headless`

which is more suitable for headless cloud environments.

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/XXYoLoong/Safety-Helmet-Detection-Modelscope.git
cd Safety-Helmet-Detection-Modelscope
```

### 2. Create a virtual environment

#### Windows

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run locally

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:7860
```

---

## Deploy to ModelScope Space

### 1. Create a new Space
Create a new project in ModelScope Space.

### 2. Configure the environment
Use the following configuration:

- SDK = `gradio`
- Gradio Version = `6.2.0`
- Image = `ubuntu22.04-py311-torch2.9.1-modelscope1.35.0`

### 3. Upload files
Upload the following files to the repository root:

- `app.py`
- `requirements.txt`
- `README.md`
- `README.en.md`

### 4. Publish the Space
Publish the Space and wait for the build to complete.

### 5. Access the app
Once the build succeeds, you can access and use the application.

---

## First Run Notes

The model will be downloaded automatically during the first run:

```text
damo/cv_tinynas_object-detection_damoyolo_safety-helmet
```

So the first inference may take longer, which is normal.

---

## Local Debugging Advice

It is strongly recommended to **run the project successfully on your local machine before uploading it to ModelScope Space**.

Reasons:

- uploading files does not immediately mean the app is fully runnable
- the actual execution result is usually visible only after publishing
- when deployment fails, debugging mainly depends on failure logs
- online debugging is much less efficient than local debugging

Please verify the following locally first:

- dependencies can be installed successfully
- the model can be loaded normally
- image upload and inference work correctly
- the result image can be returned properly

---

## Troubleshooting

### 1. No full detection interface after upload

**Symptom:**  
You cannot see a complete usable detection interface immediately after uploading code.

**Reason:**  
Uploading files does not mean the app has already run successfully. In most cases, the actual execution result appears only after publishing.

**Fix:**  
Publish the Space first, then check runtime status and logs. Local testing is strongly recommended.

---

### 2. `numpy` / `scipy` version conflict

**Symptom:**  
Errors such as `binary incompatibility` or `dtype size changed` appear at startup.

**Reason:**  
`numpy` and `scipy` versions are incompatible.

**Fix:**  
Pin dependency versions and avoid installing incompatible newer versions automatically.

---

### 3. Missing `easydict`

**Symptom:**  
Model loading fails with `No module named 'easydict'`.

**Reason:**  
TinynasDetectionPipeline depends on `easydict`.

**Fix:**  
Add the following to `requirements.txt`:

```txt
easydict==1.13
```

---

### 4. Missing `trust_remote_code=True`

**Symptom:**  
Model initialization fails and asks for `trust_remote_code`.

**Reason:**  
The model needs to execute extra code from the model repository.

**Fix:**  
Explicitly add the following inside `pipeline(...)`:

```python
trust_remote_code=True
```

---

### 5. Local Python version too new

**Symptom:**  
Installing `scipy` on Windows triggers source compilation and fails because no Fortran compiler is available.

**Reason:**  
A too-new Python version is used, such as Python 3.14.

**Fix:**  
Use:

- Python 3.10
- Python 3.11

This project recommends **Python 3.11**.

---

## Recommended Dependencies

It is recommended to pin the following versions:

```txt
gradio==6.2.0
modelscope==1.35.0
numpy==1.26.4
scipy==1.11.4
opencv-python-headless==4.10.0.84
pillow==10.4.0
easydict==1.13
```

---

## License

This project is released under the [Apache License 2.0](./LICENSE).

---

## Acknowledgements

Thanks to ModelScope for providing models, datasets, and Space deployment support.

If you are also using ModelScope, feel free to visit my profile and connect with me:  
**https://modelscope.cn/profile/yoloong**
