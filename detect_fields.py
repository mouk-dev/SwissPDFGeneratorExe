from PyPDF2 import PdfReader

def list_form_fields(pdf_path):
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()
    if not fields:
        print("❌ Aucun champ interactif trouvé.")
        return
    print("🧾 Champs détectés dans le formulaire PDF :\n")
    for field_name in fields:
        print(f" - {field_name}")

if __name__ == "__main__":
    path = input("Chemin vers le PDF : ").strip()
    list_form_fields(path)
