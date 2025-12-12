
# How to use this:
This is a command line interface application. It currently works best on Windows, with Python 3.12. 

We recommend using [UV](https://github.com/astral-sh/uv) for the installation and environment.
`pip install uv`
`uv venv`
`uv pip install -r ...\segmentClassifyProject\app\requirements.txt`

Once the environment is ready, you can use `uv run ...\segmentClassifyProject\app\main.py` to run `main.py`.
The following arguments can be given:

`-i`: 
Required. An input to process. The input must be a directory of png or jpg images. 
These can be the images with multiple sand grains that need to be segmented, or the already segmented grains.
Note: if using already segmented grains, the `-a` argument needs to be passed (and the `-s` argument can be skipped).

`-o`:
Required. The directory in which to place the outputs.

`-s`:
Required for segmentation: the directory with the segmenting model in it. 

`-c`:
Required. The directory with the classifier model or models in it.

`-a`:
Required for skipping segmentation: pass `-a` as argument if the input consists of already segmented grains. 

# example usage
`uv run "..\segmentClassifyProject\app\main.py" -i "..\input\segmented_grains" -o "..\output_Classifier" -s "..\input\model_segmenter" -c "..\input\multiple_classifier_models" -a`

`uv run "..\segmentClassifyProject\app\main.py" -i" "..\segmentClassifyProject\input_for_testing\output_Classifier\segmented_grains" -o "..\segmentClassifyProject\input_for_testing\output_Classifier" -s "..\segmentClassifyProject\input_for_testing\model_segmenter" -c "..\segmentClassifyProject\input_for_testing\multiple_models" -a`

# Models to use
Use the "model_segementer" model for the segmentation, and the 4 models in the "multiple_models" folder for classification.

Afterwards, load the outputs into the provided R script.
