def valid_phone(phone):

    return (
        phone.isdigit()
        and len(phone) == 10
    )


def valid_status(status):

    return status in [
        "Pending",
        "Approved",
        "Received",
        "Cancelled"
    ]


def calculate_total(quantity, unit_price):

    return quantity * unit_price
