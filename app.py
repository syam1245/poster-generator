from flask import Flask, render_template, request, make_response
from fpdf import FPDF

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Laptop Details", 0, 1, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 6, title, 0, 1, "L")
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    brand = request.form.get("brand")
    model = request.form.get("model")
    ram = request.form.get("ram")
    storage = request.form.get("storage")
    mrp = request.form.get("mrp")
    offer_price = request.form.get("offer_price")
    additional_offers = request.form.get("additional_offers")

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title(f"Brand: {brand}")
    pdf.chapter_body(f"Model: {model}\nRAM: {ram}\nStorage: {storage}\nMRP: {mrp}\nOffer Price: {offer_price}\nAdditional Offers: {additional_offers}")

    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=laptop_details.pdf"

    return response

if __name__ == "__main__":
    app.run(debug=True)
