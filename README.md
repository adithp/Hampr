🧺 HAMPR – Custom Gift Hamper Builder

HAMPR is a full-stack web application that allows users to build personalized gift hampers by selecting a box, adding products, decorations, and managing everything dynamically in a cart.
The platform focuses on customization, usability, and real-time updates, making the gifting experience simple and enjoyable.

🚀 Features
🛍️ User Features

Select and customize hamper boxes with different sizes

Add products, variants (size/color), and decorations

Real-time cart updates (quantity, price, volume)

Intelligent volume calculation to fit items inside the box

Dynamic price calculation (box + products + decorations)

User authentication & session-based cart handling

Responsive UI for desktop and mobile

⚙️ Admin Features

Manage boxes, box sizes, products, variants, and decorations

Upload multiple images per product

Stock management for product variants

Organized admin panel for catalog control

🧱 Tech Stack
Frontend

HTML5

CSS3

Bootstrap 5

JavaScript (Vanilla JS)

Django Template Language (DTL)

Backend

Django

Django Class-Based Views

Django ORM

Database

PostgreSQL / MySQL (configurable)

Other Tools & Libraries

Font Awesome

AOS Animations

JSON-based API communication for cart updates

📂 Project Structure
hampr/
│
├── accounts/        # Authentication & user management
├── catalog/         # Products, boxes, variants, decorations
├── cart/            # Cart logic, volume & price calculation
├── orders/          # Order handling (future-ready)
├── static/          # CSS, JS, images
├── templates/       # Django templates
├── media/           # Uploaded product images
├── manage.py
└── requirements.txt

🧠 Core Logic Highlights

Dynamic Cart System
Cart updates happen via AJAX without page reloads.

Volume Calculation
Each product/decoration contributes to box volume to prevent overflow.

Variant-Aware Products
Supports both size-based and color-based variants.

Smart Replacement Flow
Users can replace:

Only the box

Or the entire cart (box + items)

🛠️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/hampr.git
cd hampr

2️⃣ Create Virtual Environment
python -m venv env
source env/bin/activate   # Linux / Mac
env\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Update database settings in settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hampr_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

5️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser
python manage.py createsuperuser

7️⃣ Start the Server
python manage.py runserver


Open:
👉 http://127.0.0.1:8000/

📸 Screenshots

(Add screenshots of home page, product selection, cart, admin panel here)

🔮 Future Improvements

Online payment gateway integration

Order tracking system

Wishlist feature

Coupon & discount system

REST API for mobile app support

👨‍💻 Author

Adith

📍 Vadakara, Kerala

💼 Full-Stack Developer

🔗 LinkedIn

🧑‍💻 GitHub

📜 License

This project is licensed under the MIT License.
Feel free to use, modify, and distribute with proper attribution.
