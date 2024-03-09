import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xmltocsv(xmlpath, outputpath):
    xmllist = []
    for xml_file in glob.glob(os.path.join(xmlpath, "*.xml")):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for obj in root.findall("object"):
            value = (
                root.find("filename").text,
                int(root.find("size").find("width").text),
                int(root.find("size").find("height").text),
                obj.find("name").text,
                int(obj.find("bndbox").find("xmin").text),
                int(obj.find("bndbox").find("ymin").text),
                int(obj.find("bndbox").find("xmax").text),
                int(obj.find("bndbox").find("ymax").text),
            )
            xmllist.append(value)

    columns = [
        "filename",
        "width",
        "height",
        "class",
        "xmin",
        "ymin",
        "xmax",
        "ymax",
    ]
    df = pd.DataFrame(xmllist, columns=columns)
    df.to_csv(outputpath, index=None)
    print(f"Successfully converted {len(xml_list)} XML files to {outputpath}")


xmlfolders = r"C:\Users\ravee\Documents\images dataset\Czech\train\annotations\xmls"
outputcsv = r"C:\Users\ravee\Documents\images dataset\Czech\train\train_Czech.csv"
xmltocsv(xmlfolder, outputcsv)
