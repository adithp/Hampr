# HAMPR 🧺  
### Custom Gift Hamper Builder – Django Web Application

HAMPR is a full-stack web application that allows users to build **personalized gift hampers** by selecting boxes, products, variants, and decorations.  
The system handles **real-time cart updates, volume constraints, and dynamic pricing**, providing a smooth and intuitive customization experience.

---

## ✨ Key Features

- 🧺 Select hamper boxes with multiple size options  
- 🛍️ Add products with size / color variants  
- 🎀 Add decorative items to the hamper  
- 📦 Intelligent volume calculation to prevent overflow  
- 💰 Automatic price calculation (box + items)  
- 🔄 Replace box or entire cart seamlessly  
- 🔐 User authentication & session-based cart  
- 📱 Fully responsive UI  

---

## 🧑‍💻 Tech Stack

**Frontend**
- HTML5  
- CSS3  
- Bootstrap 5  
- JavaScript (Vanilla JS)  
- Django Template Language (DTL)

**Backend**
- Django  
- Class-Based Views  
- Django ORM  

**Database**
- PostgreSQL / MySQL  

---

## 📁 Project Structure

```text
hampr/
├── accounts/        # Authentication & users
├── catalog/         # Boxes, products, variants, decorations
├── cart/            # Cart logic & calculations
├── orders/          # Order workflow (extensible)
├── templates/       # Django templates
├── static/          # CSS, JS, assets
├── media/           # Uploaded images
├── manage.py
└── requirements.txt
