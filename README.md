# 🖼️ AI Image Restoration Web Application

A full-stack web application for AI-powered image restoration. Upload a degraded image and restore it using advanced computer vision and deep learning techniques.

![Tech Stack](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![Tech Stack](https://img.shields.io/badge/Flask-3.1-000000?logo=flask)
![Tech Stack](https://img.shields.io/badge/OpenCV-4.11-5C3EE8?logo=opencv)
![Tech Stack](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch)

---

## ✨ Features

- **Noise Removal** — Median filter + Non-Local Means denoising (with DnCNN AI fallback)
- **Image Deblurring** — Wiener deconvolution + unsharp masking
- **Super Resolution** — Enhanced bicubic upscaling with detail enhancement (2×)
- **Interactive Comparison** — Drag slider to compare original vs. restored
- **Download** — Save the restored image to your computer
- **Processing Timer** — See how long each restoration takes
- **Error Handling** — Graceful handling of invalid files and server errors

---

## 📁 Project Structure

```
dip project/
├── frontend/               # React (Vite) frontend
│   ├── src/
│   │   ├── App.jsx          # Main application component
│   │   ├── App.css          # Application styles
│   │   ├── index.css        # Global design system
│   │   └── components/
│   │       ├── ImageComparison.jsx   # Before/after slider
│   │       └── ImageComparison.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/                 # Flask API server
│   ├── app.py               # API endpoints
│   └── requirements.txt     # Python dependencies
├── model/                   # Image processing module
│   ├── processor.py         # Processing dispatcher
│   ├── denoise.py           # Noise removal (classical + AI)
│   ├── deblur.py            # Wiener deconvolution
│   ├── super_resolution.py  # Super resolution pipeline
│   └── dncnn.py             # DnCNN PyTorch model
└── README.md
```

---

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **pip** (comes with Python)

### 1. Clone / Navigate to the Project

```bash
cd "dip project"
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Start the Flask API server
python backend/app.py
```

The API will start at **http://localhost:5000**

### 3. Frontend Setup

Open a **new terminal**:

```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the React dev server
npm run dev
```

The app will open at **http://localhost:3000**

### 4. Use the Application

1. Open **http://localhost:3000** in your browser
2. Upload an image (drag & drop or click to browse)
3. Select a restoration type (Noise Removal / Deblurring / Super Resolution)
4. Click **Restore Image**
5. Use the slider to compare before/after
6. Click **Download** to save the restored image

---

## 🧠 Processing Methods

| Restoration Type | Method | Details |
|---|---|---|
| **Noise Removal** | NL-Means + Median Filter | OpenCV `fastNlMeansDenoisingColored` with median pre-filtering |
| **Noise Removal (AI)** | DnCNN | 17-layer residual CNN (requires pretrained weights in `model/weights/dncnn.pth`) |
| **Deblurring** | Wiener Deconvolution | Frequency-domain deconvolution + unsharp masking |
| **Super Resolution** | Enhanced Bicubic (2×) | Bicubic upscale → bilateral filter → unsharp mask → detail enhance |

### Using DnCNN Pretrained Weights

To enable AI-based denoising, place a pretrained DnCNN weights file at:

```
model/weights/dncnn.pth
```

Without this file, the system automatically falls back to the classical NL-Means method.

---

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/restore` | Upload image + type → process and return result ID |
| `GET` | `/api/image/:id/input` | Retrieve original uploaded image |
| `GET` | `/api/image/:id/output` | Retrieve processed/restored image |

### POST `/api/restore`

**Form Data:**
- `image` — Image file (PNG, JPG, BMP, TIFF, WebP; max 16 MB)
- `type` — One of: `denoise`, `deblur`, `super_resolution`

**Response:**
```json
{
  "success": true,
  "output_id": "uuid-string",
  "processing_time": 1.23,
  "restoration_type": "denoise",
  "method": "NL-Means + Median Filter (Classical)"
}
```

---

## 📋 Tech Stack

- **Frontend:** React 19, Vite, Vanilla CSS
- **Backend:** Python Flask, Flask-CORS
- **Processing:** OpenCV, NumPy, PyTorch (optional)
- **Architecture:** REST API with file-based image storage

---

## 📜 License

This project is for educational purposes.
