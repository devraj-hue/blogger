import stripe

# 🔑 Replace with your actual Stripe secret key
stripe.api_key = 'sk_test_YOUR_SECRET_KEY'

def create_checkout_session(title, price):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': title,
                },
                'unit_amount': int(price * 100),  # Convert ₹ to paise
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:5000/success',
        cancel_url='http://localhost:5000/cancel',
    )
    return session.url