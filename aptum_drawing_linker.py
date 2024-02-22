import os
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
from tqdm import tqdm
import argparse

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def add_pdf_link(folder, filename):
    return str(Path(folder) / filename)

def check_for_pdf(folder, placemark_name):
    for file in os.listdir(folder):
        if placemark_name in file:
            return file
    return None

def add_pdf_links_to_placemarks(kml_file, folder_containing_pdf):
    try:
        tree = ET.parse(kml_file)
        root = tree.getroot()
    except Exception as e:
        logging.error(f"Failed to parse KML file: {e}")
        return

    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    placemarks = list(root.findall('.//kml:Placemark', ns))

    for pm in tqdm(placemarks, desc="Processing placemarks"):
        if pm.find('kml:name', ns) is not None:
            pm_name = pm.find('kml:name', ns).text
        logging.info(pm_name)

        if pm_name is not None:
            filename = check_for_pdf(folder_containing_pdf, pm_name)
            if filename is None:
                logging.warning(f'PDF not found for {pm_name}')
                continue

            pdf_link = add_pdf_link(folder_containing_pdf, filename)

            description = pm.find('kml:description', ns)
            if description is not None:
                if "Open PDF" in description.text:
                    continue

                description.text += f'<br/><a href="file:\\\\\\{pdf_link}" target="_blank">Open Link</a>'
            else:
                description = ET.SubElement(pm, '{http://www.opengis.net/kml/2.2}description')
                description.text = f'<a href="file:\\\\\\{pdf_link}" target="_blank">Open Link</a>'

    tree.write("modified.kml", encoding='utf-8', xml_declaration=True)

def main():
    parser = argparse.ArgumentParser(description='Add PDF links to KML placemarks.')
    parser.add_argument('kml_file', help='The KML file to modify.')
    parser.add_argument('pdf_folder', help='The folder containing the PDF files.')
    parser.add_argument('--log', action='store_true', help='Enable logging.')
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(level=logging.INFO)

    add_pdf_links_to_placemarks(args.kml_file, args.pdf_folder)

    logging.info('New as-built kml saved to "modified.kml"')

if __name__ == "__main__":
    main()
