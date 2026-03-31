# ModelScope 创空间复现版：安全帽检测

这个版本是按 **魔搭社区创空间** 环境整理的可部署版本，适配：

- SDK：gradio
- Gradio：6.2.0
- 镜像：ubuntu22.04-py311-torch2.9.1-modelscope1.35.0
- 云资源：免费 CPU

## 目录结构

```text
.
├── app.py
├── requirements.txt
└── README.md
```

## 部署方式

1. 在魔搭社区新建创空间。
2. 选择 **SDK = gradio**。
3. 选择 **Gradio 版本 = 6.2.0**。
4. 选择镜像 **ubuntu22.04-py311-torch2.9.1-modelscope1.35.0**。
5. 把本目录下的 `app.py`、`requirements.txt`、`README.md` 上传到仓库根目录。
6. 等待创空间构建完成后访问即可。

## 说明

- 首次运行时会自动下载模型：
  `damo/cv_tinynas_object-detection_damoyolo_safety-helmet`
- 代码保留了你截图中的核心结构：
  - `pipeline(Tasks.domain_specific_object_detection, model=...)`
  - `OutputKeys.SCORES / LABELS / BOXES`
  - `cv2.rectangle(...)`
  - `cv2.putText(...)`
- 这里把界面写成了 `gr.Blocks`，目的是更稳地适配 Gradio 6.2.0。
- OpenCV 这里使用 `opencv-python-headless`，更适合云端无桌面环境。

## 本地调试

```bash
pip install -r requirements.txt
python app.py
```

然后访问：

```text
http://127.0.0.1:7860
```
