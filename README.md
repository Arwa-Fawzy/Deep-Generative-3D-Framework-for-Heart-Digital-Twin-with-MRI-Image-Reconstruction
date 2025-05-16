# 🫀 3dgan: High-Fidelity 3D Cardiac Image Synthesis Using GANs

## Overview

The generation of high-quality 3D cardiac images is critical for applications such as **digital twins**, **clinical simulations**, **training machine learning models**, and **diagnostic augmentation**. However, this task is often hindered by privacy constraints and the limited availability of publicly labeled medical imaging datasets.

**3dgan** addresses these challenges by implementing a **3D Generative Adversarial Network (GAN)** framework capable of synthesizing realistic volumetric heart models. The model leverages a large collection of **11,000 unlabeled normal cardiac MRI scans** to learn intricate spatial features of the heart anatomy. Using a **StyleGAN2-based teacher model**, we generate a synthetic dataset of **10,000 high-fidelity 3D cardiac images**, which serve as training data for a smaller, efficient student model through a knowledge distillation process.

This work marks the **first step toward building a personalized digital twin of the heart** by enabling the generation of **tailored heart dimensions** based on individual patient anatomy. This foundation paves the way for future clinical applications, including patient-specific diagnostics, simulation, and disease modeling.

---

## Key Features

- **3D GAN Architecture:** Employs convolutional layers, batch normalization, and LeakyReLU activation to stabilize training and enhance gradient flow for volumetric cardiac data generation.
- **Knowledge Distillation Framework:** Transfers knowledge from a large, pre-trained StyleGAN2 teacher network (30 million parameters) to a lightweight student generator (10 million parameters), maintaining high image synthesis quality while reducing computational complexity.
- **Large-Scale Preprocessing Pipeline:** Processes and standardizes **11,000 unlabeled normal cardiac MRI volumes** for consistent input to the GAN training.
- **Synthetic Dataset Generation:** Produces **10,000 synthetic 3D heart images** that capture detailed anatomical features.
- **Volumetric Rendering:** Integrates GAN outputs into **Blender**, transforming volumetric data into high-fidelity 3D heart models suitable for visualization and simulation.
- **Web Interface Integration:** Facilitates interactive visualization of generated heart models via an intuitive web platform.
- **Extensible Framework:** Designed to extend toward diseased heart anatomies and patient-specific modeling in future work.

---

## Model Architecture Details

### Teacher Model: StyleGAN2

- Implements the StyleGAN2 architecture, consisting of a **mapping network** and a **synthesis network**.
- The **mapping network** transforms a latent vector \( z \sim \mathcal{N}(0, I) \) from the latent space \( Z \) into an intermediate latent space \( W \), enabling disentangled control over generated features.
- The **synthesis network** progressively generates realistic 3D cardiac volumes from the latent representation.
- StyleGAN2 is pre-trained on the preprocessed cardiac MRI dataset and remains **frozen** during the distillation process.

### Student Model

- A smaller and computationally efficient generator network designed to replicate the teacher’s performance.
- Employs carefully designed convolutional blocks and batch normalization layers.
- Trained via knowledge distillation to **mimic both the teacher’s final output and intermediate feature representations**.
- Parameter count reduced by approximately 3× (from 30M to 10M), enabling faster inference and lower resource consumption.

![image](https://github.com/user-attachments/assets/5c48b2ea-fd4d-4643-9646-de40b6f4558b)

### Knowledge Distillation Process

- Both teacher and student models receive the **same latent vectors \( z \)** during training.
- The student network is optimized to minimize the difference between its output and the teacher’s outputs, including:
  - The final synthesized 3D images.
  - Intermediate feature maps at multiple network layers.
  - Latent space representations.
- The teacher’s parameters remain fixed, guiding the student toward accurate replication without retraining.

---

## Data Preprocessing

- Developed a robust preprocessing pipeline to handle **10,000 unlabeled normal cardiac MRI volumes**.
- Standardized all volumes to have consistent:
  - Orientation (e.g., axial slices aligned).
  - Intensity normalization to reduce inter-scan variance.
  - Spatial dimensions through resizing and cropping.
- These steps reduce noise and variability, enabling the GAN to focus on learning true anatomical structures rather than scanner artifacts or patient positioning differences.


![WhatsApp Image 2025-05-14 at 17 27 21_7263eadb](https://github.com/user-attachments/assets/aa143b34-4ecb-4605-926d-8eb94c71f6cc)



## Extracting Dimensions: Step-by-Step Summary

1. **Setup Environment**  
   Install and prepare the necessary YOLOv8 dependencies for training and inference.

2. **Organize Dataset**  
   Define and create the folder structure for training and validation images and labels following YOLO's expected format.

3. **Prepare Labels**  
   Generate dummy labels by placing a landmark at the center of each heart image to simulate ground-truth points for training.

4. **Split Dataset**  
   Randomly split the dataset into training and validation subsets.

5. **Create Data Configuration**  
   Write a configuration file specifying dataset paths and class names for YOLOv8 training.

6. **Train YOLOv8 Model**  
   Train a YOLOv8 model on the labeled heart images to detect landmark points, using a small pre-trained model for efficiency.

7. **Load Trained Model**  
   Load the best weights from the trained YOLOv8 model for prediction.

8. **Predict Landmarks**  
   Run inference on validation images to predict landmark coordinates.

9. **Extract Coordinates**  
   Retrieve the detected landmark points' (x, y) pixel coordinates from model predictions.

10. **Compute Dimension 'z'**  
    Calculate the diagonal distance \( z = \sqrt{x^2 + y^2} \) to represent a third spatial dimension for each landmark.

11. **Save to CSV**  
    Store the image names and extracted (x, y, z) coordinates in a CSV file for downstream analysis.
![image](https://github.com/user-attachments/assets/39afe07a-f4a0-446b-9c44-1a1c64295c69)

---

## Model Deployment & Visualization

- After training, the **student model** generates volumetric 3D cardiac images with explicit **X, Y, and Z pixel dimensions**.
- The volumetric outputs are imported into **Blender**, an open-source 3D graphics software, which converts them into **high-fidelity anatomical heart models**.
- These models are integrated with a **web-based interface** that supports interactive visualization, allowing users to explore synthetic heart anatomy dynamically.
- This deployment framework is intended as the **initial stage toward a full heart digital twin**, capable of supporting personalized diagnostics and simulations.
![blender_render](https://github.com/user-attachments/assets/9ebbcc31-5bd8-4357-bbed-026c75d63070)
![web_snapshot](https://github.com/user-attachments/assets/b5da3a10-fcca-4b2d-9b50-e8d0560488ee)

---

## Future Directions

- **Extension to Diseased Anatomies:** Training GAN models to synthesize cardiac images exhibiting various pathological conditions.
- **Patient-Specific Modeling:** Incorporating clinical imaging data to generate personalized cardiac digital twins tailored to individual patients.
- **Interactive Simulation Tools:** Developing diagnostic and therapeutic simulation platforms leveraging generated 3D cardiac models.
- **Improved Efficiency:** Further reducing model size and inference time while maintaining image quality.

---

## Keywords

`3D GAN` • `Cardiac Imaging` • `Medical Image Synthesis` • `Knowledge Distillation` • `StyleGAN2` • `Digital Twin` • `MRI` • `Volumetric Data` • `Blender Rendering`

---


