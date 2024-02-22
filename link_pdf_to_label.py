import os
import xml.etree.ElementTree as ET
from pathlib import Path
import logging

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
    # Parse the KML file
    tree = ET.parse(kml_file)
    root = tree.getroot()

    # Namespace dictionary for KML elements
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    # Iterate through all placemarks
    for pm in root.findall('.//kml:Placemark', ns):
        # Get placemark name if it exists
        if pm.find('kml:name', ns) is not None:
            pm_name = pm.find('kml:name', ns).text
        logging.info(pm_name)

        # Add PDF link to placemark description
        if pm_name is not None:

            # Check if PDF exists
            filename = check_for_pdf(folder_containing_pdf, pm_name)
            if filename is None:
                logging.warning(f'PDF not found for {pm_name}')
                continue

            # Define PDF link
            pdf_link = add_pdf_link(folder_containing_pdf, filename)

            description = pm.find('kml:description', ns)
            if description is not None:
                # Skip if "Open PDF" already in description
                if "Open PDF" in description.text:
                    continue

                description.text += f'<br/><a href="{pdf_link}" target="_blank">Open PDF</a>'
            else:
                description = ET.SubElement(pm, '{http://www.opengis.net/kml/2.2}description')
                description.text = f'<a href="{pdf_link}" target="_blank">Open PDF</a>'

    # Write the modified KML back to file
    tree.write("modified.kml", encoding='utf-8', xml_declaration=True)

# Example usage:
def main():
    kml_file = "asbuiltlabels.kml"
    folder_containing_pdf = r"C:\Users\Cr\As Builts\Aptum As Builts\Toronto_Mississauga"
    add_pdf_links_to_placemarks(kml_file, folder_containing_pdf)

    logging.info('New as-built kml saved to "modified.kml"')

if __name__ == "__main__":
    main()
