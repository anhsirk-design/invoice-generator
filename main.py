import os
from bill_logic import calculate_amount, calculate_total, format_inr, clean_number
from export_docx import export_bill
from export_pdf import convert_to_pdf
from datetime import date

items = []

bill_no = input("Bill Number: ")
client = input("Client Name: ")

# invoice date
date_input = input("Invoice date (press enter for today): ")
invoice_date = date_input if date_input else date.today().strftime("%d-%b-%Y")

# due date
due_date = input("Due date (press enter if none): ")

while True:

    particulars = input("Particulars: ")
    qty = input("Qty (press enter if none): ")
    rate = input("Rate: ")

    rate = clean_number(rate)

    amount = calculate_amount(qty, rate)

    items.append({
        "particulars": particulars,
        "qty": qty,
        "rate": rate,
        "amount": amount
    })

    more = input("Add more items? (y/n): ")

    if more.lower() != "y":
        break


amounts = [item["amount"] for item in items]
total = calculate_total(amounts)

print("Total:", format_inr(total))

# generate docx
docx_path = export_bill(bill_no, client, items, total, due_date, invoice_date)

# export choice
choice = input("Export format? (1 = Word, 2 = PDF): ")

if choice == "2":
    convert_to_pdf(docx_path)

    # remove the Word file
    os.remove(docx_path)

    print("PDF exported in output folder")

else:
    print("Word file exported in output folder")