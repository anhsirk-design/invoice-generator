from flask import Flask, render_template, request, send_file
from bill_logic import calculate_amount, calculate_total
from export_docx import export_bill
from export_pdf import convert_to_pdf

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "POST":

        bill_no = request.form["bill_no"]
        client = request.form["client"]
        from datetime import date

        invoice_date = request.form.get("date")

        if not invoice_date:
            invoice_date = date.today().strftime("%d-%b-%Y")

        due_date = request.form["due_date"]

        particulars = request.form.getlist("particulars")
        qtys = request.form.getlist("qty")
        rates = request.form.getlist("rate")

        items = []

        for p,q,r in zip(particulars, qtys, rates):

            if not p:
                continue

            rate = int(r)
            amount = calculate_amount(q, rate)

            items.append({
                "particulars": p,
                "qty": q,
                "rate": rate,
                "amount": amount
            })

        total = calculate_total([i["amount"] for i in items])

        docx_path = export_bill(bill_no, client, items, total, due_date, invoice_date)

        if request.form["export"] == "pdf":

            pdf_path = convert_to_pdf(docx_path)
            return send_file(pdf_path, as_attachment=True)

        return send_file(docx_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)