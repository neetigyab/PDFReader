from extractor import extract_pdf_text
from field_mapper import map_fields_to_content
from output_generator import save_to_excel

if __name__ == "__main__":
    input_pdf = "ref/New Dispute form Template check.pdf"
    output_excel = "Dispute_form_output.xlsx"

    lines = extract_pdf_text(input_pdf)
    mapped_data = map_fields_to_content(lines, input_pdf)
    save_to_excel(mapped_data, output_excel)
