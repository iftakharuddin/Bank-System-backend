import requests

def notify_ewallet(transaction):
    """Notify System A (E-wallet) about transaction success/failure via webhook."""
    
    payload = {
        "transaction_id": transaction.transaction_id,
        "status": transaction.status.value,
        "amount": transaction.amount,
        "to_wallet_id": transaction.to_wallet_id,
    }

    try:
        response = requests.post(transaction.callback_url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"Webhook notification sent successfully: {transaction.callback_url}")
        else:
            print(f"Failed to send webhook: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Webhook request failed: {e}")
