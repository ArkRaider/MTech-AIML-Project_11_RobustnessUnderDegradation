# 🔬 Project 11 — Robustness Under Degradation

**M.Tech AI/ML | Image Classification Robustness Analysis**

---

## 📌 What This Project Is About

Modern deep learning models are typically trained and evaluated on **clean, well-lit, properly formatted images**. But in the real world, image quality is rarely perfect — cameras blur, sensors add noise, lighting fails, and angles vary.

This project answers a critical question:

> **How does a pre-trained image classifier perform as image quality progressively deteriorates — and does it know when it's wrong?**

We evaluate a **pre-trained ResNet-20 model** on the **CIFAR-10** dataset by systematically applying four types of degradation at five increasing severity levels, then measuring both accuracy and the model's *confidence* in its predictions.

---

## 🗂️ Project Structure

```
MTech-AIML-Project_11_RobustnessUnderDegradation/
│
├── src/                        # Core Python modules
│   ├── model.py                # Model loading and inference
│   ├── preprocessing.py        # Image degradation functions
│   └── evaluation.py           # Metric calculation utilities
│
├── notebooks/
│   └── experiment.ipynb        # Main Jupyter notebook (run this!)
│
├── data/
│   ├── sample_data.csv         # Manifest of the 1,000 test images used
│   └── cifar-10-batches-py/    # Raw CIFAR-10 binary data (auto-downloaded)
│
├── results/
│   ├── results.csv             # Per-sample predictions and confidence scores
│   ├── comparison_table.csv    # Aggregated metrics per degradation & severity
│   └── figures/
│       └── metrics_trends.png  # Visualization plots
│
├── presentation/
│   └── 11_RobustnessUnderDegradation.pptx   # Project presentation (20 min)
│
├── create_notebook.py          # Script to (re)generate the Jupyter notebook
├── generate_presentation.py    # Script to (re)generate the .pptx file
├── requirements.txt            # Python dependencies
└── README.md                   # You are here
```

---

## 🧠 Model & Dataset

### Dataset: CIFAR-10
- **60,000** colour images, each **32×32 pixels**
- **10 classes**: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck
- We use the **test split** (10,000 images), sub-sampling **1,000 images** for speed

### Model: ResNet-20
- A 20-layer **Residual Network** designed for small images
- Loaded **pre-trained** directly from PyTorch Hub: `chenyaofo/pytorch-cifar-models`
- No additional training is performed — we evaluate the model as-is

---

## ⚙️ Degradations Applied

Each degradation is applied at **severity levels 1 through 5** (0 = clean baseline).

| Degradation | What it simulates | Technical implementation |
|---|---|---|
| **Gaussian Blur** | Lens defocus, motion blur | Radius = severity × 1.0 pixels |
| **Gaussian Noise** | Sensor noise, low-light | Noise std = severity × 10.0 |
| **Brightness Reduction** | Poor lighting, nighttime | Factor = max(0.1, 1.0 − severity × 0.15) |
| **Rotation** | Camera misalignment | Angle = severity × 15 degrees |

---

## 📊 Evaluation Metrics

| Metric | Description |
|---|---|
| **Accuracy** | % of images correctly classified |
| **Macro-F1** | F1 score averaged equally across all 10 classes |
| **Mean Confidence** | Average softmax probability of the predicted class |
| **Confidence-Accuracy Gap** | `|Mean Confidence − Accuracy|` — measures overconfidence |

> **The Confidence-Accuracy Gap is key.** A large gap means the model is frequently *wrong* but still *very sure of itself* — a dangerous property in real-world applications.

---

## 🚀 Setup & Installation

### Prerequisites
- Python **3.10 or newer**
- `pip` package manager
- (Optional but recommended) A CUDA-enabled GPU

### Step 1: Clone the repository
```bash
git clone https://github.com/ArkRaider/MTech-AIML-Project_11_RobustnessUnderDegradation.git
cd MTech-AIML-Project_11_RobustnessUnderDegradation
```

### Step 2: (Recommended) Create a virtual environment
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

This installs: `torch`, `torchvision`, `scikit-learn`, `pandas`, `matplotlib`, `seaborn`, `jupyter`, `ipykernel`, `Pillow`, `python-pptx`.

---

## ▶️ Running the Experiment

### Option A: Jupyter Notebook (Recommended)

The notebook walks you through every step interactively.

```bash
# If the notebook doesn't exist yet, generate it first:
python create_notebook.py

# Launch Jupyter
jupyter notebook notebooks/experiment.ipynb
```

Run the cells **top-to-bottom**. The notebook will:
1. Download CIFAR-10 automatically to `data/`
2. Load the pre-trained ResNet-20
3. Loop through all degradation types and severity levels
4. Compute metrics and save results to `results/`
5. Generate and display visualisation plots

> ⏱️ Expected runtime: **~5–15 minutes** on CPU, **~1–3 minutes** on GPU.

---

## 🔮 How to Use the Model to Predict on Your Own Image

You can use the `src/model.py` and `src/preprocessing.py` modules to run inference on any image of your own.

### Quick-start prediction script

```python
import torch
import torchvision.transforms as transforms
from PIL import Image
from src.model import load_model, predict
from src.preprocessing import get_degradations

# 1. Load the model
model = load_model()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 2. Load your image (must be convertible to 32x32 RGB)
image = Image.open("your_image.jpg").convert("RGB").resize((32, 32))

# 3. (Optional) Apply a degradation
#    Available: 'blur', 'noise', 'brightness', 'rotation'
#    Severity: integer from 0 (clean) to 5 (most degraded)
degradations = get_degradations()
degraded_image = degradations['blur'](image, severity=3)

# 4. Preprocess for the model (convert to tensor and normalise)
normalize = transforms.Normalize(
    mean=[0.4914, 0.4822, 0.4465],
    std=[0.2023, 0.1994, 0.2010]
)
to_tensor = transforms.ToTensor()
input_tensor = normalize(to_tensor(degraded_image)).unsqueeze(0)  # Add batch dim

# 5. Run prediction
predicted_class, confidence = predict(model, device, input_tensor)

# 6. Map class index to label
CIFAR10_CLASSES = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]
print(f"Predicted: {CIFAR10_CLASSES[predicted_class[0]]}")
print(f"Confidence: {confidence[0]*100:.1f}%")
```

> **Note:** The model was trained on **32×32 CIFAR-10 images**. If you feed it a high-resolution photo, resize it to 32×32 first. Predictions may not be meaningful on photos that don't resemble CIFAR-10 categories.

---

## 📈 Understanding the Results

After running the notebook, check:

| File | What it contains |
|---|---|
| `results/comparison_table.csv` | Summary table: one row per `(degradation, severity)` pair with all 4 metrics |
| `results/results.csv` | Full per-image log: true label, predicted label, and confidence for every image |
| `results/figures/metrics_trends.png` | Line plots showing how each metric changes as severity increases |

### What to look for in the plots
- **Accuracy/F1 dropping** steeply → model is sensitive to that degradation
- **Mean Confidence staying high** while accuracy drops → overconfidence / miscalibration
- **Confidence-Accuracy Gap widening** → the model is becoming increasingly unreliable

---

## 🔄 Regenerating Project Files

```bash
# Regenerate the Jupyter notebook
python create_notebook.py

# Regenerate the PowerPoint presentation
python generate_presentation.py
```

---

## 🗒️ Key Design Decisions

1. **Why ResNet-20?** It's a well-known, compact, CIFAR-10-native model with documented baseline accuracy (~92% on clean data), making degradation drops easy to observe.

2. **Why 1,000 images (not all 10,000)?** To keep the experiment runnable in minutes on a CPU. You can change `subset_indices = range(1000)` in the notebook to use more images.

3. **Why these 4 degradations?** They represent the most common real-world failure modes: optical (blur), electronic (noise), environmental (brightness), and geometric (rotation).

4. **Why softmax confidence as the metric?** Softmax output is the most commonly used proxy for model confidence. Its gap from accuracy reveals *miscalibration*, a well-studied problem in deep learning.

---

## 📚 References

- He et al. (2016) — *Deep Residual Learning for Image Recognition*
- Krizhevsky (2009) — *Learning Multiple Layers of Features from Tiny Images* (CIFAR-10)
- Guo et al. (2017) — *On Calibration of Modern Neural Networks*
- PyTorch Hub: [chenyaofo/pytorch-cifar-models](https://github.com/chenyaofo/pytorch-cifar-models)

---

*M.Tech AI/ML — Project 11 | Robustness Under Degradation*
