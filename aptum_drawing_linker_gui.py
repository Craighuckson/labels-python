import tkinter as tk
from tkinter import filedialog
import os
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
from tqdm import tqdm
import argparse

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def add_drawing_link(folder, filename):
    return str(Path(folder) / filename)

def check_for_drawing(folder, placemark_name):
    for file in os.listdir(folder):
        if placemark_name in file:
            return file
    return None

def add_links_to_placemarks(kml_file, as_built_folder, kml_out):
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
            filename = check_for_drawing(as_built_folder, pm_name)
            if filename is None:
                logging.warning(f'PDF not found for {pm_name}')
                continue

            drawing_link = add_drawing_link(as_built_folder, filename)

            description = pm.find('kml:description', ns)
            if description is not None:
                if "Open PDF" in description.text:
                    continue

                description.text += f'<br/><a href="file:\\\\\\{drawing_link}" target="_blank">Open Link</a>'
            else:
                description = ET.SubElement(pm, '{http://www.opengis.net/kml/2.2}description')
                description.text = f'<a href="file:\\\\\\{drawing_link}" target="_blank">Open Link</a>'

    tree.write(kml_out, encoding='utf-8', xml_declaration=True)


def main():
    # Create a root Tk window and hide it
    root = tk.Tk()
    root.withdraw()

    # Use a file dialog to get the input KML file
    kml_in = filedialog.askopenfilename(title='Select the KML file to modify',
                                        filetypes=[('KML files', '*.kml')])

    # Use a directory dialog to get the as-built folder
    as_built_folder = filedialog.askdirectory(title='Select the folder containing the as-built files')

    # Use a file dialog to get the output KML file
    kml_out = filedialog.asksaveasfilename(title='Select the modified KML file to save',
                                           defaultextension='.kml',
                                           filetypes=[('KML files', '*.kml')])

    # Check if the user cancelled any of the dialogs
    if not kml_in or not as_built_folder or not kml_out:
        return

    add_links_to_placemarks(kml_in, as_built_folder, kml_out)

    logging.info(f'New as-built kml saved to {kml_out}')

if __name__ == "__main__":
    main()
