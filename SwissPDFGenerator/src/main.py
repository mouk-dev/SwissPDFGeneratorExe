import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QSpinBox, QVBoxLayout, QFileDialog, QMessageBox
)
from faker import Faker
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import BooleanObject, NameObject

class PDFGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employment Form Generator")
        self.resize(450, 250)

        layout = QVBoxLayout()

        self.label = QLabel("Number of application forms to generate:")
        layout.addWidget(self.label)

        self.spinBox = QSpinBox()
        self.spinBox.setRange(1, 500)
        self.spinBox.setValue(5)
        layout.addWidget(self.spinBox)

        self.selectBtn = QPushButton("Select the blank PDF form")
        self.selectBtn.clicked.connect(self.select_pdf)
        layout.addWidget(self.selectBtn)

        self.previewBtn = QPushButton("Preview Data")
        self.previewBtn.clicked.connect(self.preview_data)
        layout.addWidget(self.previewBtn)

        self.generateBtn = QPushButton("Generate PDF Forms")
        self.generateBtn.clicked.connect(self.generate_forms)
        layout.addWidget(self.generateBtn)

        self.setLayout(layout)
        self.template_path = None
        self.faker = Faker()
        os.makedirs("output", exist_ok=True)

    def select_pdf(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Select a PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.template_path = file_path
            QMessageBox.information(self, "File Selected", f"Selected file: {file_path}")

    def preview_data(self):
        preview_data = {
            "Name": self.faker.name(),
            "Email Address": self.faker.email(),
            "Position you are applying for": self.faker.job(),
        }
        QMessageBox.information(self, "Preview", json.dumps(preview_data, indent=2))

    def generate_forms(self):
        if not self.template_path:
            QMessageBox.warning(self, "Error", "Please select a PDF file first.")
            return

        count = self.spinBox.value()
        data_list = []

        for i in range(1, count + 1):
            reader = PdfReader(self.template_path)
            writer = PdfWriter()

            writer._root_object.update({
                NameObject("/NeedAppearances"): BooleanObject(True)
            })

            data = {
                "Name": self.faker.name(),
                "Address": self.faker.street_address(),
                "City": self.faker.city(),
                "State": self.faker.state(),
                "ZIPPIN Code": self.faker.postcode(),
                "Phone": self.faker.phone_number(),
                "Email Address": self.faker.email(),
                "Date of Birth": self.faker.date_of_birth(minimum_age=20, maximum_age=50).strftime("%Y-%m-%d"),
                "Position you are applying for": self.faker.job(),
                "Available Start Date": self.faker.date(),
                "Desired Pay": f"${self.faker.random_int(40000, 90000)}",

                # Education
                "SchoolCollegeRow1": self.faker.company(),
                "YearRow1": str(self.faker.year()),
                "DegreeRow1": "Bachelor",
                "ResultRow1": "Passed",

                "SchoolCollegeRow2": self.faker.company(),
                "YearRow2": str(self.faker.year()),
                "DegreeRow2": "Master",
                "ResultRow2": "Passed",

                # Work Experience
                "Employer Name": self.faker.company(),
                "Designation": self.faker.job(),
                "Employment dates": f"{self.faker.date()} - {self.faker.date()}",
                "Responsibilities": self.faker.sentence(),

                "Employer Name 2": self.faker.company(),
                "Designation 2": self.faker.job(),
                "Employment dates 2": f"{self.faker.date()} - {self.faker.date()}",
                "Responsibilities 2": self.faker.sentence(),

                # References
                "1 Name": self.faker.name(),
                "Phone_2": self.faker.phone_number(),

                # Checkboxes
                "Authorized": "Yes",
                "Felony": "No",
                "Past worker": "No",
                "Empl type": "Full-Time",

                # Signature & date
                "Signature": self.faker.name(),
                "Date": self.faker.date(),
            }

            page = writer.pages[0]
            writer.append(reader)
            writer.update_page_form_field_values(page, data)

            # ✅ Forcer l'état visuel des cases à cocher
            for annot in page.get("/Annots", []):
                field = annot.get_object()
                if "/T" in field:
                    field_name = field["/T"]
                    if field_name in data:
                        value = data[field_name]
                        if value.lower() in ("yes", "on", "true", "oui"):
                            field.update({
                                NameObject("/V"): NameObject("/Yes"),
                                NameObject("/AS"): NameObject("/Yes"),
                            })
                        elif value.lower() in ("no", "off", "false", "non"):
                            field.update({
                                NameObject("/V"): NameObject("/Off"),
                                NameObject("/AS"): NameObject("/Off"),
                            })

            output_pdf = f"output/application_{i:03}.pdf"
            with open(output_pdf, "wb") as f:
                writer.write(f)

            data_list.append(data)

        with open("output/export.json", "w", encoding="utf-8") as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)

        QMessageBox.information(self, "Done", f"{count} forms generated in /output.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFGenerator()
    window.show()
    sys.exit(app.exec())
