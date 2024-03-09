import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(xml_folder_path, output_csv_path):
    """
    Converts XML annotations to a CSV file with added 'depth' column.

    Args:
        xml_folder_path (str): Path to the folder containing XML files.
        output_csv_path (str): Path to save the resulting CSV file.
    """
    xml_list = []
    for xml_file in glob.glob(os.path.join(xml_folder_path, "*.xml")):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for obj in root.findall("object"):
            # Assuming 'depth' is stored as an attribute of the 'size' element
           # depth = root.find("size").get("depth", "unknown")
            value = (
                root.find("filename").text,
                int(root.find("size").find("width").text),
                int(root.find("size").find("height").text),
               # int(root.find("size").find("depth").text),
                obj.find("name").text,
                int(obj.find("bndbox").find("xmin").text),
                int(obj.find("bndbox").find("ymin").text),
                int(obj.find("bndbox").find("xmax").text),
                int(obj.find("bndbox").find("ymax").text),
            )
            xml_list.append(value)

    column_names = [
        "filename",
        "width",
        "height",
       # "depth",  # Added depth here
        "class",
        "xmin",
        "ymin",
        "xmax",
        "ymax",
    ]
    df = pd.DataFrame(xml_list, columns=column_names)
    df.to_csv(output_csv_path, index=None)
    print(f"Successfully converted {len(xml_list)} XML files to {output_csv_path}")

# Example usage:
xml_folder = r"C:\Users\ravee\Documents\images dataset\India\train\annotations\xmls"
output_csv = r"C:\Users\ravee\Documents\images dataset\India\train\output_India.csv"
xml_to_csv(xml_folder, output_csv)
