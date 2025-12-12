import cv2
import numpy as np
from pathlib import Path
import openvino as ov
import json


def get_labels(dir):
    configpath = Path(dir).joinpath("config.json")
    with open(configpath) as p:
        config = json.load(p)
        all_full_labels = config["model_parameters"]["labels"]["all_labels"]
        all_label_names = [lab["name"] for lab in all_full_labels.values()]
    return all_label_names

def classify(input_img_dir, model_dir):
    core = ov.Core()
    model = core.read_model(model=f"{model_dir}/model.xml")
    compiled_model = core.compile_model(model=model, device_name="CPU")
    for link_to_img in Path(input_img_dir).iterdir():
        originalImg = cv2.imread(str(link_to_img))
        img = cv2.resize(originalImg, (224, 224))
        x = np.expand_dims(img, axis=3)
        x = np.transpose(x, (3,2,0,1))
        results = compiled_model.infer_new_request({0: x})
        predictions = next(iter(results.values()))
        probs = predictions.reshape(-1)
        top_1 = np.argsort(probs)[-1:][::-1]
        yield (link_to_img, get_labels(model_dir)[int(top_1)], float(probs[top_1]))


