from docxtpl import DocxTemplate
from datetime import date
import os


def export_bill(bill_no, client, items, total, due_date, invoice_date):

    template_path = "templates/bill_template.docx"

    doc = DocxTemplate(template_path)

    table_data = []

    for i, item in enumerate(items, start=1):

        table_data.append({
            "sn": i,
            "particulars": item["particulars"],
            "qty": item["qty"] if item["qty"] else "-",
            "rate": item["rate"],
            "amount": item["amount"]
        })

    context = {
        "bill_no": bill_no,
        "client": client,
        "date": invoice_date,
        "due_date": due_date if due_date else "N/A",
        "items": table_data,
        "total": total
    }

    doc.render(context)

    os.makedirs("output", exist_ok=True)
    safe_client = client.lower().replace(" ", "_")
    bill_no = str(bill_no).zfill(3)
    file_path = f"output/invoice_{bill_no}_{safe_client}.docx"
    doc.save(file_path)
    return file_path