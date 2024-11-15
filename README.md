
# Relativity `.ie` File Viewer

A lightweight Python application to parse, analyze, and export data from `.ie` files generated by Relativity. This tool provides an easy-to-use interface for inspecting job configurations, field mappings, and export settings. Useful for QC or for writing handovers.

Developed by **Lewis Bennett** – November 2024.

---

## Features

### File Parsing
- Upload `.ie` files and parse their contents, including nested JSON structures.
- Supports `.ie` files generated by Relativity for Import/Export workflows.

### File Summary
- Displays detailed metadata from the `.ie` file, including:
  - **Job Name** and **Export Type**
  - **Total Fields**
  - **Regional Settings (Date Format)** and **Long Date/Time Format**
  - **Text Precedence Settings**:
    - Order of fields used for text population.
    - Encoding and field export options.
  - **Export Settings**:
    - Native file, image, and PDF export configurations.
  - **Volume Settings**:
    - Volume prefix, start number, max size, and digit padding.
  - **Subdirectory Settings**:
    - Directory prefixes and limits for file organization.

### Field Mapping
- Displays all selected fields and their data types in a tabular format.
- Supports sorting and inspection of fields.

### Export to CSV
- Exports both the file summary and field mappings into a structured CSV file.
- The **File Summary** is added to the top of the CSV for easy reference.

---

## How to Use

1. **Upload a File**:
   - Click the **"Upload .ie File"** button.
   - Select a `.ie` file from your system.
2. **View the File Summary**:
   - The summary of the job and settings will appear under **File Summary**.
3. **Inspect Field Mapping**:
   - The selected fields and their types will appear under **Field Mapping**.
4. **Export to CSV**:
   - Click the **"Export to CSV"** button to save the parsed data to a `.csv` file.
   - The exported file will include the **File Summary** followed by the **Field Mapping**.

---

## Requirements

- Python 3.6+
- Required Libraries:
  - `pandas`
  - `tkinter`

Install dependencies using:
```bash
pip install pandas
```

---

## Running the Application

1. Save the Python script to a file (e.g., `ie_file_viewer.py`).
2. Run the script:
   ```bash
   python ie_file_viewer.py
   ```
3. Use the graphical interface to upload `.ie` files and analyze them.

---

## Example Output

### File Summary
```
Job Name: DISC012
Export Type: ProductionSet
Total Fields: 49
Date Format: en-US
Long Date/Time Format: True

Text Precedence Settings:
  Export Fields As Files: True
  Text File Encoding: 65001
  Precedence Fields (Order of Text Population):
    1. ABC DOJ Production OCR
    2. Extracted Text

Export Settings:
  Export Native Files: True
  Export Images: True
  Export PDF: False

Volume Settings:
  Volume Prefix: DISC
  Volume Start Number: 12
  Volume Max Size (MB): 999999
  Volume Digit Padding: 3

Subdirectory Settings:
  Subdirectory Start Number: 1
  Max Files Per Directory: 10000
  Image Subdirectory Prefix: IMG
  Native Subdirectory Prefix: NATIVE
  Full Text Subdirectory Prefix: TEXT
  PDF Subdirectory Prefix: PDF
  Subdirectory Digit Padding: 3
  
Field List

  Production::Begin Bates

  Production::End Bates

  ABC_PROD_Companies

  ABC-US_PROD_Custodian

  M-All Custodians

  ABC_Prod_Bates Beg Attach
  
  ABC_Prod_Bates End Attach
  
  ABC DOJ Production EPROPERTIES


```

---

## License

This tool was developed for Relativity users. No specific license applies.

Developed by **Lewis Bennett** – November 2024.
