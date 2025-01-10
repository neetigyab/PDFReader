from checkbox_detector import detect_checkboxes
import pdfplumber
import numpy as np

def parse_checkbox(lines, index, aliases, pdf_path):
    """Extract checkbox states from nearby lines in the PDF."""
    output_lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            image = np.array(page.to_image().original)
            text_lines = page.extract_text_lines()

            for alias in aliases:
                if alias.lower() in lines[index].lower():
                    for candidate_line in lines[index : index + 5]:
                        bounding_box = None
                        for text_line in text_lines:
                            if candidate_line.strip() == text_line['text'].strip():
                                bounding_box = (
                                    int(text_line['x0']),
                                    int(text_line['top']),
                                    int(text_line['x1']),
                                    int(text_line['bottom'])
                                )
                                break

                        if not bounding_box:
                            continue

                        x0, y0, x1, y1 = bounding_box
                        line_image = image[y0 - 1 : y1 + 1, x0 - 20 : x1 + 1]
                        checkbox_states, checkbox_positions = detect_checkboxes(line_image, ignored_area=None)

                        if not checkbox_positions:
                            continue
                        else:
                            for position, state in checkbox_states.items():
                                if state == "Checked":
                                    candidate_line = candidate_line.strip().split("X ", 1)[-1].split("(")[0]
                                    output_lines.append(candidate_line)
                                    break

    return output_lines if output_lines else "No marked checkbox found"
