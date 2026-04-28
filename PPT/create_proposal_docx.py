from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Add Title
title = doc.add_heading('Project Proposal', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Subtitle
subtitle = doc.add_paragraph('AI-Based Image Restoration Web Application')
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in subtitle.runs:
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)

doc.add_paragraph('') # spacing

# Course & Instructor info
p_info = doc.add_paragraph()
p_info.add_run('Course: ').bold = True
p_info.add_run('Digital Image Processing\n')
p_info.add_run('Instructor: ').bold = True
p_info.add_run('Sir Rana Adeel\n')
p_info.add_run('Date: ').bold = True
p_info.add_run('April 2026')

doc.add_heading('Group Members:', level=2)
members = [
    "Husnain Faisal (23-ST-042)",
    "Zeeshan Atif (23-ST-002)",
    "Rayyan Idrees (23-ST-045)",
    "Faseeh ul Hassan (23-ST-019)"
]
for m in members:
    doc.add_paragraph(m, style='List Bullet')

doc.add_heading('1. Introduction & Problem Statement', level=1)
p1 = doc.add_paragraph(
    "Digital images are frequently degraded by noise, motion blur, or low resolution during capture, processing, and transmission. "
    "While individual algorithms exist to tackle these specific issues, there is a distinct lack of a unified, highly accessible web tool "
    "that combines both classical computer vision techniques and modern deep learning for multi-technique image restoration. "
    "Users typically have to rely on complex, heavy desktop software to restore their photos."
)

doc.add_heading('2. Proposed Solution', level=1)
p2 = doc.add_paragraph("We propose the development of an ")
p2.add_run('"AI-Based Image Restoration Web Application"').bold = True
p2.add_run(
    " that serves as an intuitive, one-stop solution for restoring degraded images directly in the browser. "
    "The platform will be a full-stack web application combining classical Computer Vision algorithms with a "
    "DnCNN (Denoising Convolutional Neural Network) deep learning model. Users will be able to upload images (up to 16 MB) "
    "and instantly apply restoration techniques, comparing the results via a live, interactive before-and-after slider."
)

doc.add_heading('3. Core Objectives & Capabilities', level=1)
doc.add_paragraph("The system will feature three primary restoration capabilities:")

p3_1 = doc.add_paragraph(style='List Number')
p3_1.add_run("Noise Removal: ").bold = True
p3_1.add_run("A two-stage pipeline utilizing a 3x3 Median Filter and Non-Local Means (NL-Means) denoising. Includes integration of a 17-layer DnCNN model built in PyTorch for AI-powered denoising using residual learning.")

p3_2 = doc.add_paragraph(style='List Number')
p3_2.add_run("Image Deblurring: ").bold = True
p3_2.add_run("Application of Wiener Deconvolution in the frequency domain via FFT, coupled with unsharp masking to effectively sharpen edges and reverse motion blur.")

p3_3 = doc.add_paragraph(style='List Number')
p3_3.add_run("Super Resolution: ").bold = True
p3_3.add_run("Enhancement of low-resolution images using Bicubic Interpolation, followed by Bilateral Filtering (for edge-preserving smoothing) and detail enhancement.")

doc.add_heading('4. System Architecture & Tech Stack', level=1)
doc.add_paragraph("The project will follow a robust three-tier client-server design:")

p4_1 = doc.add_paragraph(style='List Bullet')
p4_1.add_run("Frontend (Presentation Layer): ").bold = True
p4_1.add_run("React 19 + Vite\n").bold = True
p4_1.add_run("Features: Drag & drop file upload, custom CSS clip-path before/after comparison slider, and real-time processing metrics.")

p4_2 = doc.add_paragraph(style='List Bullet')
p4_2.add_run("Backend API (Application Layer): ").bold = True
p4_2.add_run("Python Flask\n").bold = True
p4_2.add_run("Features: RESTful endpoints (/api/restore, etc.), CORS configuration, and secure file handling/routing.")

p4_3 = doc.add_paragraph(style='List Bullet')
p4_3.add_run("Processing Engine (Data Layer): ").bold = True
p4_3.add_run("OpenCV + PyTorch\n").bold = True
p4_3.add_run("Features: Execution of core image transformations, matrix math, and inference for the deep learning models.")

doc.add_heading('5. Expected Outcomes & Deliverables', level=1)
doc.add_paragraph(
    "The final deliverable will be a functional, fast, and user-friendly web application capable of processing "
    "multiple image formats (PNG, JPG, BMP, TIFF, WebP). Operations are targeted to be highly performant, averaging "
    "between 1.0 to 2.0 seconds per restoration."
)

doc.add_heading('6. Future Scope', level=1)
doc.add_paragraph("While the core objectives cover immediate restoration needs, future work may include:")
future = [
    "Training the DnCNN model on the comprehensive BSD68 dataset.",
    "Integrating ESRGAN or Real-ESRGAN for state-of-the-art super-resolution.",
    "Implementing blind deblurring (automatic kernel estimation).",
    "Adding batch processing capabilities and deploying the application to scalable cloud infrastructure (AWS/Docker)."
]
for f in future:
    doc.add_paragraph(f, style='List Bullet')

doc.save('Project_Proposal.docx')
print("Successfully created Project_Proposal.docx")
