from checkbox_parser import parse_checkbox
from checkbox_detector import detect_checkboxes, visualize_checkboxes
import pdfplumber
import numpy as np
from config import field_mappings, checkbox_fields

def map_fields_to_content(lines, pdf_path):
    """Map fields to their respective content in the PDF."""
    mapped_data = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            image = np.array(page.to_image().original)

            # Define ignored area for the first page (e.g., top 150px height)
            ignored_area = (0, 0, image.shape[1], 425) if page_number == 1 else None
            checkbox_states, checkbox_positions = detect_checkboxes(image, ignored_area)

            # Visualize checkboxes for the current page
            visualize_checkboxes(image, checkbox_positions, checkbox_states, page_number)

            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue

                # Check if line matches any field
                for field, aliases in field_mappings.items():
                    # Only assign if the field is not already in mapped_data
                    if field not in mapped_data and any(alias.lower() in line.lower() for alias in aliases):
                        if field in checkbox_fields:
                            mapped_data[field] = parse_checkbox(lines, i, aliases, pdf_path)
                        else:
                            if i + 1 < len(lines) and "_" in lines[i + 1]:
                                mapped_data[field] = "n/a"
                            else:
                                if field == "When was the last time you used your card":
                                    if pdf_path == "ref/New Dispute form Template check.pdf":
                                        mapped_data[field] = lines[i + 2] + " " + lines[i + 5]
                                        lines.pop(i+1)
                                        lines.pop(i+2)
                                        lines.pop(i+3)
                                        lines.pop(i+4)
                                        lines.pop(i+5)
                                    else:
                                        mapped_data[field] = lines[i + 2] + " " + lines[i + 4]
                                        lines.pop(i+1)
                                        lines.pop(i+2)
                                        lines.pop(i+3)
                                        lines.pop(i+4)
                                elif field == "Reason for dispute":
                                    t = lines[i + 1].split(" ")
                                    mapped_data[field] = t[-2] + " " + t[-1]
                                else:
                                    mapped_data[field] = lines[i + 1].strip() if i + 1 < len(lines) else "Not Found"

    return mapped_data
