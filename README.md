# ⚖️ E-Vakeel Platform

A **Django-powered web platform** designed to provide quick and easy access to legal services and resources online.  
Built with **HTML, CSS, JavaScript, and Django**, the platform aims to connect clients with legal professionals, manage case-related information, and enhance user experience with a clean, intuitive interface.

---

## 📌 Features

- 📝 **User-Friendly Interface** – Simple navigation for clients and lawyers.
- 👨‍⚖️ **Lawyer Profiles** – View details, expertise, and contact options for registered lawyers.
- 📂 **Case Management** – Store and track case details securely.
- 🔍 **Search & Filter** – Quickly find lawyers based on specialization or location.
- 📧 **Contact & Enquiry Forms** – Easy communication between clients and lawyers.
- 📊 **Interactive Data Visualization** – Uses **Google Charts** for legal data insights.
- 🔒 **Authentication System** – Secure login/logout and account management.

---

## 🛠️ Tech Stack

**Frontend:**  
- HTML5  
- CSS3  
- JavaScript 
- Google Charts (for data visualization)

**Backend:**  
- Django (Python)  
- SQLite3 (default) or any Django-supported database

---


## 🚀 Live Demo

🔗 **[Watch Live Demo](https://www.linkedin.com/posts/virendrachvan_datavisualization-googlecharts-html-activity-7213809570622623746-1Oqg?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD10HoMBfYKsBhIaGz-b00jgW6fHgXMutvg)**

---

## ⚙️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/e-vakeel.git
cd e-vakeel

# Create virtual environment
python -m venv venv
source venv/bin/activate     # On macOS/Linux
venv\Scripts\activate        # On Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
