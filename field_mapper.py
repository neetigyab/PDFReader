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
                                    collected_lines = []
                                    for j in range(i + 1, len(lines)):
                                        next_line = lines[j].strip()
                                        # Check if the next line is a new field
                                        if any(alias.lower() in next_line.lower() for alias in field_mappings.keys() if alias != "Date"):
                                            break
                                        #Removing unwanted text from line
                                        cleaned_line = re.sub(r"(Date:|Time:|_)", "", next_line)
                                        # Add the cleaned line to the collected content
                                        if cleaned_line.strip():
                                            collected_lines.append(cleaned_line)

                                    # Join collected lines to store as the field value
                                    mapped_data[field] = " ".join(collected_lines) if collected_lines else "Not Found"

                                    for j in range(i + 1, len(lines)):
                                        lines.pop(j)
                                        if any(alias.lower() in next_line.lower() for alias in field_mappings.keys() if alias != "Date"):
                                            break

                                elif field == "Reason for dispute":
                                    next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
    
                                    # Maintain a set of already assigned substrings
                                    assigned_substrings = set()
                                    for value in mapped_data.values():
                                        if isinstance(value, str):
                                            assigned_substrings.update(value.split())

                                    # Remove assigned substrings, numerical values, and special characters (except '/')
                                    filtered_line = " ".join(
                                        word for word in next_line.split()
                                        if word not in assigned_substrings and not re.search(r'[^\w/]', word) and not re.search(r'\d', word)
                                    )
    
                                    # Assign the cleaned line to the field
                                    mapped_data[field] = filtered_line if filtered_line else "Not Found"
                                    
                                else:
                                    mapped_data[field] = lines[i + 1].strip() if i + 1 < len(lines) else "Not Found"

    return mapped_data
