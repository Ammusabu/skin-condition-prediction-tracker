# Skin Condition Prediction & Progression Analysis System
<img width="1920" height="1096" alt="image" src="https://github.com/user-attachments/assets/eae59705-09a6-4dad-a71c-85f7cb9e0ce8" />

Skin conditions such as acne, eczema, rosacea, keratosis, and carcinoma are **progressive in nature** and require continuous monitoring to evaluate disease evolution and treatment effectiveness. However, most existing AI-based dermatological systems focus only on **single-image classification**, lacking mechanisms for **severity quantification** and **longitudinal progression analysis**.

This project presents an **AI-driven end-to-end dermatological system** that integrates **multi-class skin condition prediction**, **quantitative severity assessment**, and **temporal progression tracking** into a unified framework.

---

## 🚩 Problem Statement
- Traditional AI dermatology models provide **point-in-time diagnosis only**
- No reliable way to measure **severity change over time**
- Limited support for tracking **treatment response and disease progression**

---

## 💡 Proposed Solution
A two-phase AI system that:
1. Predicts skin conditions from images using a CNN-based model  
2. Quantifies severity using a hybrid scoring mechanism  
3. Tracks disease progression longitudinally across multiple sessions  

---

## 🧠 System Overview
The system consists of three core components:

### 1️⃣ Skin Condition Classification
- CNN-based multi-class image classifier
- Identifies conditions such as acne, eczema, rosacea, keratosis, and carcinoma
- Backbone architecture: **MobileNetV2**
- Input size: **224 × 224 RGB images**

### 2️⃣ Severity Assessment
Severity is computed using a **hybrid scoring mechanism** that combines:
- Model prediction confidence
- User-reported symptom intensity (pain, itching, redness, spread)

This enables **quantitative severity measurement** rather than qualitative labeling.

### 3️⃣ Progression Analysis
- Persistent session-based data storage
- Temporal trend analysis across multiple days
- Automatically categorizes condition state as:
  - **Improving**
  - **Stable**
  - **Worsening**

This allows evaluation of **treatment effectiveness over time**.

---

## 📊 Visualization & Dashboard
- Interactive dashboards built using **Gradio and Plotly**
- Displays:
  - Severity trends over time
  - Progress timelines
  - Session-wise analysis
- Designed for intuitive interpretation by non-technical users

---

## 🚀 Model Training & Deployment
- Model training performed on **Google Colab**
- Deployed using **Gradio on Hugging Face Spaces**
- Real-time inference with persistent tracking support

---

## 🛠 Tools & Technologies
- **Programming:** Python  
- **Deep Learning:** TensorFlow / Keras  
- **Data Processing:** NumPy, Pandas  
- **Visualization:** Plotly  
- **Deployment:** Gradio, Hugging Face Spaces  

---

## 📁 Repository Structure
skin-condition-prediction-tracker/
├── training/
│ └── model_training_colab.ipynb
├── model/
│ ├── skin_model.h5
│ ├── class_labels.json
│ └── model_info.json
├── src/
│ ├── preprocess.py
│ ├── model_predict.py
│ ├── tracker.py
│ ├── analysis_plots.py
│ └── utils.py
├── app.py
├── requirements.txt
└── README.md

---

## 🔗 Live Demo
👉 Hugging Face Space: **https://huggingface.co/spaces/ammusabu/skin_condition_tracker1**

---

## 📌 Key Highlights
- End-to-end AI system (training → deployment → monitoring)
- Focus on **progressive disease tracking**, not just diagnosis
- Suitable for **research, clinical decision support, and smart healthcare applications**

---

## ⚠️ Disclaimer
This system is intended for **educational and research purposes only** and is **not a substitute for professional medical diagnosis**.
