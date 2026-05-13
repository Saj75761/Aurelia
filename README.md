# AURELIA | Luxury Menswear Digital Experience

Aurelia is a premium, high-end e-commerce platform designed for the modern gentleman. It combines a sophisticated high-fashion aesthetic with a modern technical architecture, featuring an AI-driven concierge and a cloud-native backend.

## 🔗 Live Demo
**View the live application here:** [https://aurelia-252442990659.us-central1.run.app](https://aurelia-252442990659.us-central1.run.app)

---

## ✨ Features

*   **AI Concierge**: An integrated concierge service that assists customers with fabric details, tailoring inquiries, and style consultations.
*   **Premium UI/UX**: A high-end interface utilizing glassmorphism, refined typography, and smooth reveal animations for a boutique-like experience.
*   **Dynamic Product Catalog**: Real-time filtering and category management powered by a FastAPI backend.
*   **Responsive Design**: Fully optimized for a seamless experience across desktop, tablet, and mobile devices.
*   **Secure Checkout**: A multi-step checkout simulation with order confirmation and real-time validation.

## 🛠️ Technical Stack

*   **Backend**: Python, [FastAPI](https://fastapi.tiangolo.com/)
*   **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
*   **DevOps**: Docker, [Google Cloud Run](https://cloud.google.com/run)
*   **Styling**: Premium Custom CSS (Glassmorphism, CSS Variables)

## 🚀 Local Development

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Saj75761/Aurelia.git
   cd Aurelia
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**:
   ```bash
   python main.py
   ```
   *The site will be available at http://localhost:8080*

## 🐳 Docker Deployment

You can also run the project using Docker:

```bash
docker build -t aurelia-app .
docker run -p 8080:8080 aurelia-app
```

---

## 📜 License
This project is for portfolio purposes. All rights reserved.
