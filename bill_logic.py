import re


def clean_number(value):
    # remove everything except digits
    cleaned = re.sub(r"[^\d]", "", str(value))

    if cleaned == "":
        return 0

    return int(cleaned)


def format_inr(amount):
    # convert number to ₹15,000/- format
    formatted = "{:,.0f}".format(amount)
    return f"₹{formatted}/-"


def calculate_amount(qty, rate):

    rate = clean_number(rate)

    if qty == "" or qty is None:
        return rate

    qty = clean_number(qty)

    return qty * rate


def calculate_total(items):
    return sum(items)