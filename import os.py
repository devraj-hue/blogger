import os
from flask import jsonify

# Replace with your actual webhook secret from Stripe dashboard
STRIPE_WEBHOOK_SECRET = 'whsec_YOUR_WEBHOOK_SECRET'

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError as e:
        logging.error("Webhook signature verification failed.")
        return jsonify(success=False), 400

    # ✅ Handle successful payment
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        logging.info(f"Payment successful for session: {session['id']}")
        # You can unlock blog access here or store payment info

    return jsonify(success=True), 200
    ngrok http 5000
    https://your-ngrok-url/webhook