ORDER_EMAIL_CONFIG = {

    # ---- ORDER FLOW ----
    "ORDER_COMPLETED": {
        "subject": "Your order is confirmed 🎉",
        "status": "Order Confirmed",
        "message": """
        <p>Your order has been successfully placed.</p>
        <p>We are preparing your items with care.</p>
        """
    },

    "ORDER_SHIPPED": {
        "subject": "Your order is on the way 🚚",
        "status": "Shipped",
        "message": """
        <p>Your order has been shipped.</p>
        <p>It will reach you soon.</p>
        """
    },

    "ORDER_DELIVERED": {
        "subject": "Order delivered successfully ✅",
        "status": "Delivered",
        "message": """
        <p>Your order has been delivered.</p>
        <p>We hope you love your purchase ❤️</p>
        """
    },

    # ---- RETURN FLOW ----
    "RETURN_REJECTED": {
        "subject": "Return request rejected ❌",
        "status": "Return Rejected",
        "message": """
        <p>We’re sorry to inform you that your return request has been rejected.</p>
        <p>If you need more clarification, please contact our support team.</p>
        """
    },

    "RETURN_PICKUP": {
        "subject": "Return pickup scheduled 📦",
        "status": "Return Pickup Scheduled",
        "message": """
        <p>Your return pickup has been scheduled.</p>
        <p>Please keep the product ready in its original packaging.</p>
        """
    },

    "RETURN_REFUNDED": {
        "subject": "Refund processed successfully 💸",
        "status": "Amount Refunded",
        "message": """
        <p>Your refund has been processed successfully.</p>
        <p>The amount will reflect in your account within 5–7 business days.</p>
        """
    },
}
