# Project Proposal: AI-Based Image Restoration Web Application

**Course:** Digital Image Processing
**Instructor:** Sir Rana Adeel
**Date:** April 2026

**Group Members:**
1. Husnain Faisal (23-ST-042)
2. Zeeshan Atif (23-ST-002)
3. Rayyan Idrees (23-ST-045)
4. Faseeh ul Hassan (23-ST-019)

---

## 1. Introduction & Problem Statement
Digital images are frequently degraded by noise, motion blur, or low resolution during capture, processing, and transmission. While individual algorithms exist to tackle these specific issues, there is a distinct lack of a unified, highly accessible web tool that combines both classical computer vision techniques and modern deep learning for multi-technique image restoration. Users typically have to rely on complex, heavy desktop software to restore their photos.

## 2. Proposed Solution
We propose the development of an **"AI-Based Image Restoration Web Application"** that serves as an intuitive, one-stop solution for restoring degraded images directly in the browser. The platform will be a full-stack web application combining classical Computer Vision algorithms with a DnCNN (Denoising Convolutional Neural Network) deep learning model. Users will be able to upload images (up to 16 MB) and instantly apply restoration techniques, comparing the results via a live, interactive before-and-after slider.

## 3. Core Objectives & Capabilities
The system will feature three primary restoration capabilities:

1. **Noise Removal:** 
   - A two-stage pipeline utilizing a 3x3 Median Filter (to remove salt-and-pepper noise) and Non-Local Means (NL-Means) denoising.
   - Integration of a 17-layer DnCNN model built in PyTorch for AI-powered denoising using residual learning (predicting the noise residual rather than the clean image directly).
2. **Image Deblurring:** 
   - Application of Wiener Deconvolution in the frequency domain via FFT, coupled with unsharp masking to effectively sharpen edges and reverse motion blur.
3. **Super Resolution:** 
   - Enhancement of low-resolution images using Bicubic Interpolation, followed by Bilateral Filtering (for edge-preserving smoothing) and detail enhancement.

## 4. System Architecture & Tech Stack
The project will follow a robust three-tier client-server design:

*   **Frontend (Presentation Layer):** **React 19 + Vite**
    *   Features: Drag & drop file upload, custom CSS clip-path before/after comparison slider, and real-time processing metrics (time taken, method used).
*   **Backend API (Application Layer):** **Python Flask**
    *   Features: RESTful endpoints (`/api/restore`, etc.), CORS configuration, and secure file handling/routing.
*   **Processing Engine (Data Layer):** **OpenCV + PyTorch**
    *   Features: Execution of core image transformations, matrix math, and inference for the deep learning models.

## 5. Expected Outcomes & Deliverables
The final deliverable will be a functional, fast, and user-friendly web application capable of processing multiple image formats (PNG, JPG, BMP, TIFF, WebP). Operations are targeted to be highly performant, averaging between 1.0 to 2.0 seconds per restoration. 

## 6. Future Scope
While the core objectives cover immediate restoration needs, future work may include:
*   Training the DnCNN model on the comprehensive BSD68 dataset.
*   Integrating ESRGAN or Real-ESRGAN for state-of-the-art super-resolution.
*   Implementing blind deblurring (automatic kernel estimation).
*   Adding batch processing capabilities and deploying the application to scalable cloud infrastructure (AWS/Docker).
