from checkbox_detector import detect_checkboxes
import pdfplumber
import numpy as np

def get_line_coordinates(line_text, pdf_path):
    """
    Finds the bounding box coordinates of a given line of text on a PDF page using pdfplumber.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                bool = 0 
                # Extract text with positional data
                text_data = page.extract_text_lines()

                for item in text_data:
                    # Normalize the text for comparison
                    extracted_text = item["text"].strip().lower()
                    target_text = line_text.strip().lower()

                    if extracted_text == target_text:
                        # Extract bounding box coordinates
                        x0 = int(item["x0"])
                        y0 = int(item["top"])
                        x1 = int(item["x1"])
                        y1 = int(item["bottom"])
                        pg = page_number
                        bool = 1
                if bool == 1:
                    break
                else: 
                    continue
            return x0, y0, x1, y1, pg
    except Exception as e:
        #print(f"Error in get_line_coordinates: {e}")
        return None


def parse_checkbox(lines, index, aliases, pdf_path):
    """
    Extract checkbox states from nearby lines and return text of the line
    containing a checked checkbox across all pages in the PDF.
    """
    output_lines = []  # Collect results from all pages

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Convert the page image to a NumPy array
            image = np.array(page.to_image().original)

            # Extract all text lines with bounding boxes
            text_lines = page.extract_text_lines()

            for alias in aliases:
                if alias.lower() in lines[index].lower():
                    # # Get coordinates for lines[index] and lines[index+5]
                    start_coords = get_line_coordinates(lines[index], pdf_path)

                    if "_" in lines[index + 4]:
                        end_coords = get_line_coordinates(lines[index + 3], pdf_path)
                    else:
                        end_coords = get_line_coordinates(lines[index + 4], pdf_path)

                    if not start_coords or not end_coords:
                        print("Error: Unable to determine coordinates for target lines.")

                    start_top, start_bottom, start_pg = start_coords[1], start_coords[3], start_coords[4]
                    end_top, end_bottom, end_pg = end_coords[1], end_coords[3], end_coords[4]
                    
                    # Process the next 4 lines
                    for candidate_line in lines[index : index + 5]:
                        # Find bounding box of the candidate line
                        bounding_box = None
                        for text_line in text_lines:
                            if "_" not in text_line['text'].strip():
                                # Compare text_line['top'] with the range
                                if (
                                    start_top <= text_line['top'] <= end_bottom
                                    and candidate_line.strip() == text_line['text'].strip()
                                    and page_number == start_pg == end_pg
                                ):
                                    bounding_box = (
                                        int(text_line['x0']),
                                        int(text_line['top']),
                                        int(text_line['x1']),
                                        int(text_line['bottom'])
                                    )
                                    break

                        if not bounding_box:
                            continue

                        # Crop the image to the bounding box of the line
                        x0, y0, x1, y1 = bounding_box
                        line_image = image[y0 - 1 : y1 + 1, x0 - 20 : x1 + 1]

                        # Detect checkboxes in the line image
                        checkbox_states, checkbox_positions = detect_checkboxes(line_image)
                        
                        if not checkbox_positions:
                            continue  # No checkbox found in this line
                        else:
                            for position, state in checkbox_states.items():
                                if state == "Checked":
                                    # Extract and clean the candidate line text
                                    candidate_line = candidate_line.strip().split("X ", 1)[-1].split("(")[0]
                                    output_lines.append(candidate_line)
                                    break  # No need to check further for this line
                                else:
                                    continue

    # Return results after processing all pages
    output_words =', '.join(output_lines)
    return output_words if output_lines else "n/a"
