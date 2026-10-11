# Project 11: Robustness Under Degradation

**M.Tech in Artificial Intelligence and Machine Learning**  
**Image Classification Robustness Analysis**

## 1. Project Overview

Deep learning models are generally evaluated on clean images with good lighting and minimal noise. However, real-world images often contain imperfections caused by camera blur, sensor noise, poor lighting, or changes in viewing angles. These factors can affect the accuracy and reliability of image classification models.

The objective of this project is to study how a pre-trained image classification model performs when the quality of its input images gradually deteriorates. In addition to measuring classification accuracy, we examine whether the model remains confident in its predictions even when it starts making incorrect classifications.

For this experiment, we use a pre-trained ResNet-20 model on the CIFAR-10 dataset. Four types of image degradation are applied at five different severity levels, and the resulting predictions are evaluated using accuracy, Macro-F1 score, mean confidence, and the confidence-accuracy gap.

The experiment helps us understand the limitations of image classification models and the importance of evaluating their reliability under imperfect input conditions.

## 2. Project Structure

```text
MTech-AIML-Project_11_RobustnessUnderDegradation/
│
├── src/
│   ├── model.py
│   ├── preprocessing.py
│   └── evaluation.py
│
├── notebooks/
│   └── experiment.ipynb
│
├── data/
│   ├── sample_data.csv
│   └── cifar-10-batches-py/
│
├── results/
│   ├── results.csv
│   ├── comparison_table.csv
│   └── figures/
│       └── metrics_trends.png
│
├── presentation/
│   └── 11_RobustnessUnderDegradation.pptx
│
├── create_notebook.py
├── generate_presentation.py
├── requirements.txt
└── README.md
```

### Main files

- `src/model.py`: Loads the pre-trained model and performs inference.
- `src/preprocessing.py`: Contains the functions used to apply image degradations.
- `src/evaluation.py`: Calculates the evaluation metrics.
- `notebooks/experiment.ipynb`: Contains the main experiment and analysis.
- `data/sample_data.csv`: Stores the manifest of the selected test images.
- `results/results.csv`: Stores individual predictions and confidence scores.
- `results/comparison_table.csv`: Contains aggregated metrics for each degradation and severity level.
- `results/figures/metrics_trends.png`: Contains plots showing how the evaluation metrics change with degradation severity.
- `create_notebook.py`: Generates the experiment notebook.
- `generate_presentation.py`: Generates the project presentation.

## 3. Dataset and Model

### Dataset: CIFAR-10

CIFAR-10 is a widely used image classification dataset containing 60,000 colour images of size 32 × 32 pixels. The dataset consists of ten classes:

- Airplane
- Automobile
- Bird
- Cat
- Deer
- Dog
- Frog
- Horse
- Ship
- Truck

The dataset contains 50,000 training images and 10,000 test images. In this project, we use a subset of 1,000 test images to reduce the computational cost and keep the experiment manageable on a CPU.

### Model: ResNet-20

ResNet-20 is a compact convolutional neural network based on the residual learning architecture. It uses shortcut connections to help information flow through the network and is commonly used for image classification tasks involving small images such as CIFAR-10.

The pre-trained model is loaded from the `chenyaofo/pytorch-cifar-models` repository through PyTorch. We evaluate the model without additional training or fine-tuning.

This allows us to focus on the effect of image degradation rather than changes introduced during model training.

## 4. Image Degradation Methods

Four types of degradation are applied to the test images. Each degradation is evaluated at severity levels from 1 to 5, with severity 0 representing the original, unmodified image.

| Degradation | Purpose | Implementation |
|---|---|---|
| Gaussian Blur | Simulates lens defocus and reduced image sharpness | Blur radius = severity × 1.0 pixels |
| Gaussian Noise | Simulates sensor noise and low-light conditions | Noise standard deviation = severity × 10.0 |
| Brightness Reduction | Simulates poor lighting and darker environments | Factor = max(0.1, 1.0 − severity × 0.15) |
| Rotation | Simulates changes in camera orientation | Angle = severity × 15 degrees |

For each degradation, the model is evaluated at all five severity levels. The clean images are also evaluated to establish a baseline for comparison.

This setup allows us to observe how different types of image distortion affect the model and whether some degradations have a greater impact than others.

## 5. Evaluation Metrics

We use four metrics to analyse the model's performance.

**Accuracy:** Measures the percentage of images classified correctly.

**Macro-F1 Score:** Calculates the F1 score independently for each class and averages the scores equally across all ten classes. This helps evaluate performance across different categories.

**Mean Confidence:** Measures the average softmax probability assigned to the model's predicted class. It indicates how confident the model is in its predictions, although it does not necessarily represent the probability that a prediction is correct.

**Confidence-Accuracy Gap:** Measures the difference between mean confidence and accuracy, with both expressed on the same scale.

A large positive gap can indicate that the model is more confident than its actual performance justifies. For example, if mean confidence is 85% but accuracy is 60%, the gap is 25 percentage points.

This metric provides a simple indication of potential overconfidence. However, it is not a complete calibration metric, and a more detailed calibration analysis would require additional measures such as Expected Calibration Error (ECE).

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or newer
- pip package manager
- A CUDA-enabled GPU is optional but recommended for faster execution

### Step 1: Clone the repository

```bash
git clone https://github.com/ArkRaider/MTech-AIML-Project_11_RobustnessUnderDegradation.git
cd MTech-AIML-Project_11_RobustnessUnderDegradation
```

### Step 2: Create a virtual environment

Creating a virtual environment helps keep the project's dependencies separate from other Python projects.

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS or Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

The project uses the following libraries:

- PyTorch and torchvision
- scikit-learn
- pandas
- matplotlib and seaborn
- Jupyter and ipykernel
- Pillow
- python-pptx

The exact dependencies and versions are specified in `requirements.txt`.

## 7. Running the Experiment

The Jupyter notebook is the recommended way to run the experiment because it presents the workflow step by step.

### Step 1: Generate the notebook if necessary

```bash
python create_notebook.py
```

### Step 2: Launch Jupyter Notebook

```bash
jupyter notebook notebooks/experiment.ipynb
```

### Step 3: Execute the notebook

Run the notebook cells in order. The experiment will:

1. Download the CIFAR-10 dataset if it is not already available.
2. Load the pre-trained ResNet-20 model.
3. Select 1,000 test images.
4. Apply the four degradation methods at each severity level.
5. Generate predictions and calculate the evaluation metrics.
6. Save the individual predictions and aggregated results.
7. Generate plots showing the changes in model performance.

The expected execution time is approximately 5–15 minutes on a CPU and 1–3 minutes on a GPU. Actual runtime depends on the hardware and software environment.

## 8. Making Predictions on a Custom Image

The model can also be used to make predictions on an individual image. The image must be converted to RGB format and resized to 32 × 32 pixels before inference.

The following example shows how to apply Gaussian blur and obtain a prediction.

```python
import torch
import torchvision.transforms as transforms
from PIL import Image

from src.model import load_model, predict
from src.preprocessing import get_degradations

# Load the pre-trained model
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = load_model()
model = model.to(device)

# Load and resize the input image
image = Image.open("your_image.jpg")
image = image.convert("RGB").resize((32, 32))

# Apply an optional degradation
degradations = get_degradations()
degraded_image = degradations["blur"](
    image, severity=3
)

# Convert the image to a normalized tensor
normalize = transforms.Normalize(
    mean=[0.4914, 0.4822, 0.4465],
    std=[0.2023, 0.1994, 0.2010]
)

to_tensor = transforms.ToTensor()

input_tensor = normalize(
    to_tensor(degraded_image)
).unsqueeze(0)

# Run inference
predicted_class, confidence = predict(
    model, device, input_tensor
)

# Display the prediction
CIFAR10_CLASSES = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
]

print(
    f"Predicted: {CIFAR10_CLASSES[predicted_class[0]]}"
)
print(f"Confidence: {confidence[0] * 100:.1f}%")
```

**Note:** The model is trained on CIFAR-10 images, which contain small, low-resolution objects. Predictions on ordinary high-resolution photographs may not be meaningful, even after resizing them to 32 × 32 pixels, particularly when the photographs differ significantly from the CIFAR-10 dataset.

## 9. Understanding the Results

After completing the experiment, the following files can be used to analyse the results.

| File | Description |
|---|---|
| `results/comparison_table.csv` | Aggregated metrics for every degradation and severity level |
| `results/results.csv` | Individual predictions, actual labels, predicted labels, and confidence scores |
| `results/figures/metrics_trends.png` | Plots showing performance trends as degradation severity increases |

The main objective is to compare the performance of the model on clean images with its performance on degraded images.

The following patterns are particularly useful to investigate:

- **Declining accuracy and Macro-F1:** Indicates that the degradation is affecting classification performance.
- **High confidence despite declining accuracy:** Suggests that the model may remain overconfident when its predictions become less reliable.
- **Increasing confidence-accuracy gap:** Indicates a growing difference between the model's average confidence and its observed accuracy.
- **Differences between degradation types:** Help identify which image distortions are most challenging for the model.

The results should be interpreted from the actual experimental measurements rather than assuming that every degradation will affect the model in the same way.

## 10. Regenerating Project Files

The notebook and presentation can be regenerated using the provided Python scripts.

To regenerate the notebook:

```bash
python create_notebook.py
```

To regenerate the PowerPoint presentation:

```bash
python generate_presentation.py
```

The presentation is intended to support a project discussion of approximately 20 minutes.

## 11. Design Decisions

**Why ResNet-20?**

ResNet-20 is a relatively lightweight model designed for CIFAR-10-style images. Its compact architecture makes it suitable for experiments that need to run on ordinary hardware. Published implementations can achieve approximately 90% or higher accuracy on clean CIFAR-10 test data, although the exact baseline depends on the checkpoint and evaluation setup.

**Why use 1,000 images instead of the entire test set?**

Using a subset reduces execution time and makes it easier to run the experiment repeatedly. The subset can be increased to obtain a more comprehensive evaluation, at the cost of additional computation.

**Why select these four degradation methods?**

Blur, noise, brightness reduction, and rotation represent different sources of variation in image data. They allow us to study the effects of reduced sharpness, sensor noise, poor illumination, and geometric transformations within the same experimental framework.

**Why measure softmax confidence?**

Softmax probabilities are commonly used as a simple indicator of model confidence. Comparing the average confidence with actual accuracy helps reveal cases where the model appears confident despite making incorrect predictions. Since average confidence alone does not fully measure calibration, additional calibration metrics can be incorporated in future work.

## 12. Conclusion

This project investigates the robustness of a pre-trained image classification model under different types and levels of image degradation. By evaluating accuracy, Macro-F1 score, mean confidence, and the confidence-accuracy gap, the experiment examines both classification performance and the reliability of model predictions.

The results can help identify image conditions under which the model becomes less accurate and determine whether its confidence reflects its actual performance. The same experimental approach can also be extended to other model architectures, larger datasets, additional corruption types, and more comprehensive calibration metrics.

## 13. References

1. He, K., Zhang, X., Ren, S., and Sun, J. (2016). *Deep Residual Learning for Image Recognition.* Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR).

2. Krizhevsky, A. (2009). *Learning Multiple Layers of Features from Tiny Images.* University of Toronto.

3. Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks.* Proceedings of the 34th International Conference on Machine Learning (ICML).

4. Chen Yaofo. *PyTorch CIFAR Models.* GitHub repository: https://github.com/chenyaofo/pytorch-cifar-models

5. PyTorch Documentation: https://pytorch.org/docs/
