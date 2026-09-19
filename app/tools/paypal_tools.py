def create_invoice(customer: str, amount: float):
    return {
        "status": "success",
        "message": f"Invoice of ${amount:.2f} created for {customer}"
    }


def get_sales_report(month: str):
    return {
        "status": "success",
        "month": month,
        "total_sales": 12500.00
    }


def check_dispute(user_id: str):
    return {
        "status": "success",
        "user_id": user_id,
        "dispute_open": True
    }


def send_payment(customer: str, amount: float):
    return {
        "status": "success",
        "message": f"Payment of ${amount:.2f} sent to {customer}"
    }