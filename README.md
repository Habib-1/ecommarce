# 🛍️ Step Forward — Full Stack E-commerce Website (React + Django)

Step Forward is a full-stack **E-commerce web application** built with **React.js (Frontend)** and **Django REST Framework (Backend)**.  
It allows customers to browse products, add them to the cart, place orders, and make secure payments.  
Admins can manage products, categories, and orders efficiently through the Django admin panel.

---

## 🚀 Features

### 🧑‍💻 Customer Features
- User Registration & Login (JWT Authentication)
- Browse products by category
- Product Search and Filter
- Add / Remove items from cart
- Manage Wishlist (will be added)
- Checkout and Order placement
- Order History and Order Tracking
- Profile Management (Update Name, Email, etc.)
- Secure Online Payment(will be added)

### 🛠️ Admin Features
- Manage products, categories, and stock
- Manage user accounts and orders
- Update order status (Pending → Shipped → Delivered)
- Dashboard analytics (optional)

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | React.js, Axios, React Router, Tailwind CSS |
| **Backend** | Django, Django REST Framework |
| **Database** | PostgreSQL | SQLite(default)
| **Authentication** | JWT (Simple JWT) | dj-rest-auth(token based)
| **Payment Gateway** | Cash on delivary | 
| **Deployment** | Not Yet | 

---

## ⚙️ Installation & Setup

### 1️⃣ Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate     # For Windows
source venv/bin/activate  # For macOS/Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

### 1️⃣ Frontend Setup
cd frontend
npm install
npm run dev

🔮 Future Enhancements
- Product Reviews and Ratings
- Secure payment method
- Email Notification System
- Real-time Order Tracking with WebSocket / Django Channels
- Manage Wishlist





