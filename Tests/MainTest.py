import pdfplumber
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re

# Define fields and mappings (unchanged from original code)
fields = [
    "Name",
    "Account number",
    "Last 4 digits of the card",
    "Transaction date",
    "Amount",
    "Merchant name",
    "Date you lost your card",
    "Time you lost your card",
    "Date you realized your card was stolen",
    "Time you realized your card was stolen",
    "When was the last time you used your card",
    "Last transaction amount",
    "Where do you normally store your card",
    "Where do you normally store your PIN",
    "Other items that were stolen",
    "Officer name",
    "Report number",
    "Suspect name",
    "Date",
    "Contact number",
    "Reason for dispute",
    #Add fields as per requirement...
]  # Same as your provided code
checkbox_fields = [
    "Transaction not authorized",
    "My card was",
    "Do you know who made the transaction",
    "Have you given permission to anyone to use your card",
    "Have you filed police report",
    #Add fields as per requirement...
]  # Same as your provided code
field_mappings = {
    "Name" : ["Your Name"],
    "Account number" : ["Account#"],
    "Last 4 digits of the card" : ["Last 4 digits of the card#"],
    "Transaction date" : ["Transaction date"],
    "Amount" : ["Amount$"],
    "Merchant name" : ["Merchant name"],
    "Transaction not authorized" : ["SECTION 1: TRANSACTION NOT AUTHORIZED"], #checkbox entry
    "My card was" : ["My card was (Select one):"], #checkbox entry
    "Date you lost your card"  : ["What DATE did you lose your card?"],
    "Time you lost your card"  : ["What TIME did you lose your card?"],
    "Date you realized your card was stolen"  : ["What DATE did you realize your card was missing?"],
    "Time you realized your card was stolen"  : ["What TIME did you realize your card was missing?"],
    "Do you know who made the transaction" : ["Do you know who made these transactions? (Select one):"], #checkbox entry
    "Have you given permission to anyone to use your card" : ["Have you given permission to anyone to use your card? (Select one):"], #checkbox entry
    "When was the last time you used your card" : ["When was the last time you used your card?"],
    "Last transaction amount" : ["Amount: $"],
    "Where do you normally store your card" : ["Where do you normally store your card?"],
    "Where do you normally store your PIN" : ["Where do you normally store your PIN?"],
    "Other items that were stolen" : ["Please list other items that were lost or stolen, including your mobile phone or any', 'additional cards (if applicable):"],
    "Have you filed police report" : ["Have you filed a police report? (Select one)"], #checkbox entry
    "Officer name" : ["District/OWicer name:", "District/OVicer name:"],
    "Report number" : ["Report number:"],
    "Suspect name" : ["Suspect name:"],
    "Date" : ["Date:"],
    "Contact number" : ["Contact number (during the hours of 8am-5pm PST):"],
    "Reason for dispute" : ["Transaction date Amount Merchant Name Reason for dispute"],
    #Add field mappings as per requirement...
}  # Same as your provided code






def extract_pdf_text(pdf_path):
    """Extract all text lines from a PDF."""
    try:
        lines = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                page_lines = text.splitlines()
                if text:
                    print(f"--- Page {page_number} Text ---\n{page_lines}\n{'-'*50}")
                lines.extend(page_lines)
        return lines
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []






def detect_checkboxes(image, ignored_area=None):
    """Detect checkboxes and determine if they are checked or unchecked, ignoring specified areas."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    checkbox_states = {}
    checkbox_positions = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 0.8 <= aspect_ratio <= 1.5 and 10 <= w <= 30 and 10 <= h <= 30:
            # Skip checkboxes in the ignored area
            if ignored_area and (ignored_area[0] <= x <= ignored_area[0] + ignored_area[2] and
                                 ignored_area[1] <= y <= ignored_area[1] + ignored_area[3]):
                continue
            roi = gray[y+2:y+h-2, x+2:x+w-2]
            non_zero = cv2.countNonZero(roi)
            checkbox_states[(x, y)] = "Unchecked" if non_zero > (w * h * 0.45) else "Checked"
            checkbox_positions.append((x, y, w, h))

    return checkbox_states, checkbox_positions






def visualize_checkboxes(image, checkbox_positions, checkbox_states, page_number):
    """Visualize all detected checkboxes on the image."""
    for (x, y, w, h) in checkbox_positions:
        state = checkbox_states.get((x, y), "Unchecked")
        color = (0, 255, 0) if state == "Checked" else (0, 0, 255)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(f"Checkboxes Detected on Page {page_number}")
    plt.axis("off")
    plt.show()











def get_line_coordinates(line_text, pdf_path):
    """
    Finds the bounding box coordinates of a given line of text on a PDF page using pdfplumber.

    Args:
        line_text (str): The text of the line to search for.
        page (pdfplumber.page.Page): The page object from pdfplumber.

    Returns:
        tuple or None: Coordinates (x0, y0, x1, y1) if found, otherwise None.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                bool = 0 
                # Extract text with positional data
                text_data = page.extract_text_lines()
                #print(f"--- Page {page_number} Text ---\n")

                for item in text_data:
                    # Normalize the text for comparison
                    extracted_text = item["text"].strip().lower()
                    target_text = line_text.strip().lower()
                    #print(f"checking for '{target_text}' in : '{extracted_text}'")

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

                #print(f"Line '{line_text}' not found on the page.")
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
                    
                    #print(f"coordinates for {alias} : ",start_coords)
                    #print(f"coordinates for end point of {alias} : ",end_coords)

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
                        checkbox_states, checkbox_positions = detect_checkboxes(line_image, ignored_area=None)
                        
                        if not checkbox_positions:
                            plt.imshow(line_image)
                            plt.title(f"Checkbox NOT detected on page {page_number} in this line for field {alias}")
                            plt.show()
                            continue  # No checkbox found in this line
                        else:
                            plt.imshow(line_image)
                            plt.title(f"Checkbox detected on page {page_number} in this line for field {alias}")
                            plt.show()
                            for position, state in checkbox_states.items():
                                if state == "Checked":
                                    plt.imshow(line_image)
                                    plt.title(f"Marked Checkbox on this line on page {page_number} for field {alias}")
                                    plt.show()
                                    # Extract and clean the candidate line text
                                    candidate_line = candidate_line.strip().split("X ", 1)[-1].split("(")[0]
                                    output_lines.append(candidate_line)
                                    break  # No need to check further for this line
                                else:
                                    continue

    # Return results after processing all pages
    #print(output_lines)
    output_words =', '.join(output_lines)
    if output_lines:
        return output_words
    return "n/a"






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
                                    output_lines = []
                                    for x in range (i + 1, len(lines)):
                                        next_line = lines[x].strip() if x < len(lines) else ""
    
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
                                        if filtered_line not in output_lines:
                                            output_lines.append(filtered_line)
                                    
                                    output_words =', '.join(output_lines)
                                    # Assign the cleaned line to the field
                                    mapped_data[field] = output_words if output_lines else "Not Found"
                                
                                else:
                                    mapped_data[field] = lines[i + 1].strip() if i + 1 < len(lines) else "Not Found"
    
    # Debugging output
    print("--- Mapped Fields and Content ---")
    for field, content in mapped_data.items():
        print(f"{field}: {content}")
    print("-" * 50)

    return mapped_data






def save_to_excel(mapped_data, filename):
    """Save the mapped data to an Excel file."""
    df = pd.DataFrame(list(mapped_data.items()), columns=["Field", "Value"]).T
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")






if __name__ == "__main__":
    input_pdf = "ref/New Dispute form Template check 1.pdf" #Replace with required pdf form
    output_excel = "Dispute_form_output.xlsx"

    lines = extract_pdf_text(input_pdf)
    mapped_data = map_fields_to_content(lines, input_pdf)
    save_to_excel(mapped_data, output_excel)
