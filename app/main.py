import argparse
from datetime import datetime
from classifier import classify
from segmenter import segment
from pathlib import Path

def build_argparser():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(add_help=False)
    args = parser.add_argument_group("Options")
    args.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )
    args.add_argument(
        "-i",
        "--input_img_dir",
        required=True,
        help="Required. An input to process. The input must be a directory of png or jpg images.\
         Note: if using segmented images, use -a ",
    )
    args.add_argument(
        "-a",
        "--segmented_images",
        required=False,
        default=False,
        action='store_true',
        help="Use if the input folder is full of already segmented images"
    )
    args.add_argument(
        "-o",
        "--output_dir",
        required=True,
        help="Required. A director to place outputs.",
    )
    args.add_argument(
        "-s",
        "--model_segmenter",
        action="store",
        help="Required for segmentation. The folder with the SEGMENTER model in it.",
        required=False
    )
    args.add_argument(
        "-c",
        "--model_classifier",
        action="store",
        help="Required. The folder with the CLASSIFIER model(s) in it.",
        required=True
    )
    return parser

def main():
    args = build_argparser().parse_args()
    if args.segmented_images:
        segmented_folder = Path(args.input_img_dir)
    else:
        segmented_folder = Path(args.output_dir).joinpath("segmented_grains")
        segmented_folder.mkdir(parents=True,exist_ok=True)
        for input_image in Path(args.input_img_dir).iterdir():
            segment(input_image, args.model_segmenter, segmented_folder)
    if len([f for f in Path(args.model_classifier).iterdir() if f.is_dir()]) > 0:
        models_classifier = [model for model in Path(args.model_classifier).iterdir() if model.is_dir()]
    else:
        models_classifier = [Path(args.model_classifier)]

    for classifier_model in models_classifier:
        classifier_name = classifier_model.name
        with open(f"{args.output_dir}/{Path(args.input_img_dir).name}_{classifier_name}_predictions.csv", "w") as f:
            f.write("File,Class1,Confidence1,\n")
            for prediction in classify(segmented_folder, classifier_model):
                f.write(str(prediction[0]))
                f.write(",")
                f.write(str(prediction[1]))
                f.write(",")
                f.write(str(prediction[2]))
                f.write("\n")

if __name__ == "__main__":
    main()


