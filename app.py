from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
import gradio as gr
import cv2
import numpy as np


MODEL_ID = 'damo/cv_tinynas_object-detection_damoyolo_safety-helmet'
_detector = None


def get_detector():
    global _detector
    if _detector is None:
        _detector = pipeline(
            Tasks.domain_specific_object_detection,
            model=MODEL_ID,
            trust_remote_code=True
        )
    return _detector


def draw_detection_result(img, detection_result, score_threshold=0.3):
    scores = detection_result.get(OutputKeys.SCORES, [])
    labels = detection_result.get(OutputKeys.LABELS, [])
    boxes = detection_result.get(OutputKeys.BOXES, [])

    assert img is not None, 'image is None'

    for score, label, box in zip(scores, labels, boxes):
        if float(score) < score_threshold:
            continue

        x1, y1, x2, y2 = map(int, box)

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            img,
            f'{label} {score:.2f}',
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

    return img


def safety_helmet_detect(image):
    if image is None:
        return None

    image = np.array(image)

    if image.ndim == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    detector = get_detector()
    result = detector(image)
    output_image = draw_detection_result(image.copy(), result)
    return output_image


demo = gr.Interface(
    fn=safety_helmet_detect,
    inputs=gr.Image(type='pil', label='上传图片'),
    outputs=gr.Image(type='numpy', label='检测结果'),
    title='安全帽检测',
    description='上传一张图片，自动检测图中人员是否佩戴安全帽。'
)

if __name__ == '__main__':
    demo.launch(server_name='0.0.0.0', server_port=7860)