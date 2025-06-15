# Image-Based Machine Learning Model: Training and Deployment in Python

This repository demonstrates a simple image classification pipeline using a Convolutional Neural Network (CNN) trained on "Dogs" and "Cats" images, along with an extensible deployment setup for AI-powered applications.

## Table of Contents

- [Overview](#overview)
- [Components](#components)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Security](#security)
- [License](#license)

## Overview

This project provides a complete workflow for building and deploying a generative AI system. It includes:

- **model-training:** Training a CNN model on a two-class image dataset ("Dogs" and "Cats").
- **application:** A FastAPI-based service for loading the trained model and serving image predictions.

## Components

### [model-training](model-training)

Trains a CNN model to classify images as either "Dog" or "Cat".

### [application](application)

A FastAPI application that predicts the category of uploaded images.

## Getting Started

### Prerequisites

**Clone the repository:**

```bash
git clone https://github.com/vcse59/GenerativeAI.git
cd GenerativeAI
git checkout feature-cnn-model-training-deployment
```

### Native Setup

#### Navigate to the repository root:

- **Unix/Linux/macOS:**
  ```bash
  cd "$(git rev-parse --show-toplevel)"
  ```
- **PowerShell (Windows):**
  ```bash
  cd (git rev-parse --show-toplevel)
  ```
- **Command Prompt (Windows):**
  ```bash
  for /f "delims=" %i in ('git rev-parse --show-toplevel') do cd "%i"
  ```

#### Create and activate a Python virtual environment:

- **Windows (Command Prompt):**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
- **Unix/Linux/macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

1. **Download the image dataset from [Kaggle](https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset):**
  - Extract the archive and place the "Dog" and "Cat" folders inside `model-training\dataset\`.

    - For example, you may initially have only 10 images each for Dog and Cat in `model-training\dataset\`, but it is recommended to use a larger number of images for better model accuracy.

2. **Split the dataset into training and validation sets (80/20 split):**
   ```bash
   pip install split-folders
   cd model-training
   split-folders dataset --ratio .8 .2 --move
   ```

3. **Install dependencies for model training:**
   ```bash
   cd ..
   pip install -r model-training\requirements.txt
   ```


4. **Train the model (in a terminal with the virtual environment activated):**
   ```bash
   python model-training\train_model.py
   ```
   Training may take 25-40 minutes depending on dataset size. The trained model will be saved as `models/model.h5`.

5. **Install dependencies for the FastAPI application (in a new terminal with the virtual environment activated):**
   ```bash
   pip install -r application\requirements.txt
   ```

6. **Start the FastAPI application:**
   ```bash
   uvicorn application.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Usage

- Visit http://localhost:8000/docs to access the API documentation. Use the `/predict` endpoint to upload a "Dog" or "Cat" image and receive a prediction.

## Security

For security policies, vulnerability reporting, and best practices, see [SECURITY.md](./SECURITY.md).

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
