import cv2
import matplotlib.pyplot as plt
import numpy as np
import openvino as ov
from pathlib import Path


def segment(single_image_path, model_path, output_folder):
    core = ov.Core()
    model_xml_path = Path(model_path).joinpath("model.xml")
    model = core.read_model(model=model_xml_path)
    compiled_model = core.compile_model(model=model, device_name="CPU")
    image = cv2.imread(str(single_image_path))
    input_layer_ir = compiled_model.input(0)
    output_layer_boxes = compiled_model.output(0)
    output_layer_mask = compiled_model.output(2)
    image_h, image_w, _ = image.shape
    N, C, H, W = input_layer_ir.shape
    resized_image = cv2.resize(image, (W, H))
    input_image = np.expand_dims(
        resized_image.transpose(2, 0, 1), 0
    )
    result = compiled_model([input_image])

    for i, box in enumerate(result[output_layer_boxes]):
        x1, y1, x2, y2, confidence = box
        x1 = int(x1*(image_w/W))
        x2 = int(x2*(image_w/W))
        y1 = int(y1*(image_h/H))
        y2 = int(y2*(image_h/H))
        boxed_sandgrain = image[y1:y2, x1:x2]
        mask = result[output_layer_mask][i]
        threshold = 0.35 #this seems to be the best threshold
        larger_mask = cv2.resize(mask, (boxed_sandgrain.shape[1], boxed_sandgrain.shape[0]))
        larger_mask = cv2.cvtColor(larger_mask,cv2.COLOR_GRAY2RGB)
        segmented_sandgrain = np.where(larger_mask>threshold, boxed_sandgrain, 0)
        cv2.imwrite(f"{output_folder}/{Path(single_image_path).name}_{str(i+1).zfill(3)}.png", segmented_sandgrain)

