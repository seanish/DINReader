from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import fitz
import re
import pandas as pd
import sys
import os


# Receiving the file path and output path from the command line
folder_path = sys.argv[1]
output_path = sys.argv[2]

# List all files in the folder
files = os.listdir(folder_path)

for file in files:

    # Construct the full file path
    file_path = os.path.join(folder_path, file)
    print(file_path)

    # Opening the PDF and converting to images
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
    else:
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            print(f"Failed to open file: {file_path}")
            print(f"Error: {e}")

    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        pix.save(f'{output_path}/page_{i}.png')

    # OCR the image
    if os.path.exists(f'{output_path}/page_0.png'):
        ocrd_text = pytesseract.image_to_string(Image.open(f'{output_path}/page_0.png'))
        # process ocrd_text as needed
    else:
        print(f"Image file not found: {output_path}/page_0.png")

    #Searching for the drug code
    re.findall(r'\d+', ocrd_text)

    candidates = re.findall(r'\d+', ocrd_text)

    candidates = [int(item) for item in candidates]

    print(candidates)

    #Loading the drug info file

    drugInfo = pd.read_csv('./drugproductinfo/drug.txt', sep=',', names=['Drug Code', 'Product Categorization', 'Class', 'DIN', 'Brand Name', 'Descriptor', 'Pediatric Flag', 'Accession Number', 'Number of AIS', 'Last Update Date', 'AI Group Number', 'Class F', 'Brand Name F', 'Descriptor F'])

    print(drugInfo)

    #Finding the drug code in the drug info file and exporting the info to a csv
    matches = pd.DataFrame(columns=['DIN', 'Brand Name', 'isValid', 'Location'])
    for candidate in candidates:
        if drugInfo['DIN'].isin([candidate]).any():
            brandName = drugInfo.loc[drugInfo['DIN'] == candidate, 'Brand Name'].iloc[0]
            new_row = {'DIN': candidate, 'Brand Name': brandName, 'isValid': True, 'Location': file}
            new_row_df = pd.DataFrame([new_row])
            matches = pd.concat([matches, new_row_df], ignore_index=True)


matches.to_excel(f'{output_path}/output.xlsx', index=False)