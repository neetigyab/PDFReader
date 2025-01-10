# PDF Form Processing Tool

This project is a modular tool designed for extracting, processing, and saving data from form-like PDF documents. The tool detects and processes textual and checkbox elements in PDF files, maps fields to corresponding content, and exports the results to an Excel file.

## Features
- Extract text and checkbox data from PDFs.
- Map form fields to their corresponding values.
- Visualize detected checkboxes on PDF pages.
- Save mapped data to an Excel file.

## Project Structure

### **Packages and Modules**

#### 1. **`pdf_extractor`**
- **`extractor.py`**
  - `extract_pdf_text(pdf_path)`: Extracts all text lines from a PDF document.

#### 2. **`checkbox_detector`**
- **`checkbox_detector.py`**
  - `detect_checkboxes(image, ignored_area=None)`: Detects checkboxes in a given image and determines whether they are checked or unchecked.
  - `visualize_checkboxes(image, checkbox_positions, checkbox_states, page_number)`: Visualizes detected checkboxes and their states on the image.

#### 3. **`checkbox_parser`**
- **`checkbox_parser.py`**
  - `parse_checkbox(lines, index, aliases, pdf_path)`: Extracts checkbox states from nearby lines in the PDF.

#### 4. **`field_mapper`**
- **`field_mapper.py`**
  - `map_fields_to_content(lines, pdf_path)`: Maps fields to their respective content based on the extracted text and detected checkboxes.

#### 5. **`output_saver`**
- **`output_generator.py`**
  - `save_to_excel(mapped_data, filename)`: Saves the mapped data to an Excel file.

#### 6. **`config`**
- **`config.py`**
  - `fields`: A list of fields expected in the PDF.
  - `checkbox_fields`: A subset of fields specifically for checkboxes.
  - `field_mappings`: A dictionary mapping field names to possible aliases in the PDF.

---

## Libraries Utilized
1. **`pdfplumber`**: For extracting text and images from PDF documents.
2. **`OpenCV`**: For detecting and visualizing checkboxes.
3. **`numpy`**: For handling image arrays and numerical operations.
4. **`matplotlib`**: For visualizing checkboxes.
5. **`pytesseract`**: For Optical Character Recognition (OCR) when necessary.
6. **`pandas`**: For saving data to an Excel file.

---

## Manual Inputs and Configuration

### 1. **Fields of Expected Form Elements**
- **`fields`**: Define all possible fields that the PDF form may contain. This list must be updated to include any new fields introduced in the form layout.
- Example:
  ```python
  fields = ["Name", "Address", "Date of Birth", "Phone Number"]
  ```

### 2. **Field Mappings**
- **`field_mappings`**: Define mappings to evaluate differences between actual field names in the form and expected field names.
- Example:
  ```python
  field_mappings = {
      "Name": ["Full Name", "Name of Applicant"],
      "Address": ["Residential Address", "Home Address"],
  }
  ```

### 3. **Checkbox Fields**
- **`checkbox_fields`**: Specify fields that require checkbox processing.
- Example:
  ```python
  checkbox_fields = ["Terms and Conditions", "Subscription Opt-in"]
  ```

---

## Updating for New Form Layouts
1. **Add New Fields**: Update the `fields` list in `config/config.py` to include any new fields present in the updated form layout.
2. **Update Field Mappings**: Extend `field_mappings` with aliases for new or renamed fields.
3. **Update Checkbox Fields**: Add any new checkbox-related fields to the `checkbox_fields` list.

---

## Usage

### 1. Extract Text from PDF
The `extract_pdf_text` function extracts lines of text from the PDF.
```python
lines = extract_pdf_text("path/to/pdf")
```

### 2. Map Fields to Content
Map the extracted lines to the predefined fields using `map_fields_to_content`.
```python
mapped_data = map_fields_to_content(lines, "path/to/pdf")
```

### 3. Save Data to Excel
Save the mapped data to an Excel file using `save_to_excel`.
```python
save_to_excel(mapped_data, "output.xlsx")
```

---

## Example Workflow

1. Place the PDF file in the project directory.
2. Run the main script:
   ```bash
   python main.py
   ```
3. View the extracted and processed data in the output Excel file.

---

## Notes
- Ensure that any updates to the form layout are reflected in the `fields`, `field_mappings`, and `checkbox_fields` in `config/config.py`.
- Make sure all required libraries are installed before running the script:
  ```bash
  pip install pdfplumber opencv-python numpy matplotlib pytesseract pandas
  ```

