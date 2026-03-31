from __future__ import annotations

from typing import Any

import cv2
import gradio as gr
import numpy as np
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# 与截图一致的安全帽检测模型
MODEL_ID = 'damo/cv_tinynas_object-detection_damoyolo_safety-helmet'

_detector = None


def get_detector():
    """懒加载检测器，避免创空间启动阶段阻塞过久。"""
    global _detector
    if _detector is None:
        _detector = pipeline(
            task=Tasks.domain_specific_object_detection,
            model=MODEL_ID,
        )
    return _detector


def _safe_text(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode('utf-8', errors='ignore')
    return str(value)


# 可视化检测结果
# 基本保持你截图里的写法：scores / labels / boxes + cv2.rectangle + cv2.putText

def show_image_object_detection_auto_result(img: np.ndarray, detection_result: dict[str, Any]) -> np.ndarray:
    scores = detection_result[OutputKeys.SCORES]
    labels = detection_result[OutputKeys.LABELS]
    bboxes = detection_result[OutputKeys.BOXES]

    assert img is not None, 'Image is None!!!'

    draw_img = img.copy()
    if not draw_img.flags['C_CONTIGUOUS']:
        draw_img = np.ascontiguousarray(draw_img)

    # Gradio 传入 RGB，OpenCV 绘制前转 BGR
    draw_img = cv2.cvtColor(draw_img, cv2.COLOR_RGB2BGR)

    for score, label, box in zip(scores, labels, bboxes):
        x1, y1, x2, y2 = map(int, box)
        label_text = _safe_text(label)

        cv2.rectangle(draw_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(
            draw_img,
            f'{float(score):.2f}',
            (x1, max(y1 - 8, 18)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            lineType=8,
        )
        cv2.putText(
            draw_img,
            label_text,
            (x1, min(y2 + 24, draw_img.shape[0] - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            lineType=8,
        )

    return cv2.cvtColor(draw_img, cv2.COLOR_BGR2RGB)


# 安全帽检测

def safety_helmet_detect(image: np.ndarray):
    if image is None:
        raise gr.Error('请先上传一张图片。')

    detector = get_detector()

    # 与截图逻辑保持一致：RGB -> BGR 后送入检测器
    result = detector(np.ascontiguousarray(image[..., ::-1]))
    output_image = show_image_object_detection_auto_result(image, result)
    return output_image


with gr.Blocks(title='安全帽检测') as demo:
    gr.Markdown('# 安全帽检测')
    gr.Markdown('上传施工现场图片，自动检测图中目标是否佩戴安全帽。')

    with gr.Row():
        input_image = gr.Image(type='numpy', label='上传图片')
        output_image = gr.Image(type='numpy', label='检测结果')

    detect_btn = gr.Button('开始检测', variant='primary')
    clear_btn = gr.ClearButton([input_image, output_image], value='清空')

    detect_btn.click(
        fn=safety_helmet_detect,
        inputs=input_image,
        outputs=output_image,
    )


if __name__ == '__main__':
    demo.queue()
    demo.launch(server_name='0.0.0.0', server_port=7860)
