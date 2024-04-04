import cadquery as cq
import tkinter as tk
from tkinter import simpledialog, filedialog
import random
import os
import pandas as pd
import json
import xml.etree.ElementTree as ET

def create_shape(shape_type, dimension, file_path_step, file_path_stl):
    if shape_type == "box":
        shape = cq.Workplane("XY").box(*dimension)
    elif shape_type == "cylinder":
        shape = cq.Workplane("XY").circle(dimension[0]).extrude(dimension[1])
    elif shape_type == "hexagon":
        shape = cq.Workplane("XY").polygon(6, dimension[0]).extrude(dimension[1])
    elif shape_type == "sphere":
        shape = cq.Workplane("XY").sphere(dimension[0])
    
    # Exporting as STEP file
    cq.exporters.export(shape, file_path_step, exportType='STEP')
    # Exporting as STL file
    cq.exporters.export(shape, file_path_stl, exportType='STL')

def save_to_excel(shape_type, dimension, excel_path):
    shape_data = {'Shape': shape_type, **dimension}
    df = pd.DataFrame([shape_data])
    df.to_excel(excel_path, index=False)

def save_to_json(shape_type, dimension, json_path):
    shape_data = {'Shape': shape_type, **dimension}
    with open(json_path, 'w') as f:
        json.dump(shape_data, f, indent=4)

def save_to_xml(shape_type, dimension, xml_path):
    shape_data = ET.Element("ShapeData")
    shape_type_element = ET.SubElement(shape_data, "Type")
    shape_type_element.text = shape_type

    for dim, value in dimension.items():
        dim_element = ET.SubElement(shape_data, dim)
        dim_element.text = str(value)

    tree = ET.ElementTree(shape_data)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)

def generate_random_dimensions(shape_type):
    if shape_type == "box":
        return {'length': random.uniform(1, 10), 'width': random.uniform(1, 10), 'height': random.uniform(1, 10)}
    elif shape_type in ["cylinder", "hexagon"]:
        return {'radius': random.uniform(1, 5), 'height': random.uniform(1, 10)}
    elif shape_type == "sphere":
        return {'radius': random.uniform(1, 5)}

def generate_shapes():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    num_shapes = simpledialog.askinteger("Input", "Enter number of shapes to create:", parent=root)
    data_format = simpledialog.askstring("Input", "Enter data format (excel, json, xml):", parent=root)
    directory = filedialog.askdirectory(title="Select Folder to Save Files", parent=root)
    root.destroy()

    shape_types = ["box", "cylinder", "hexagon", "sphere"]

    for i in range(1, num_shapes + 1):
        shape_type = random.choice(shape_types)
        dimension = generate_random_dimensions(shape_type)
        step_file_name = f"{shape_type}{i}_basicshape_fraunhofer.step"
        stl_file_name = f"{shape_type}{i}_basicshape_fraunhofer.stl"
        data_file_name = f"{shape_type}{i}_basicshape_fraunhofer.{data_format}"
        step_file_path = os.path.join(directory, step_file_name)
        stl_file_path = os.path.join(directory, stl_file_name)
        data_file_path = os.path.join(directory, data_file_name)

        create_shape(shape_type, list(dimension.values()), step_file_path, stl_file_path)

        if data_format == 'excel':
            save_to_excel(shape_type, dimension, data_file_path)
        elif data_format == 'json':
            save_to_json(shape_type, dimension, data_file_path)
        elif data_format == 'xml':
            save_to_xml(shape_type, dimension, data_file_path)
        else:
            print(f"Unknown data format: {data_format}")
            continue

        print(f"Created {shape_type} shape {i} with dimensions {dimension} and saved as {step_file_name}, {stl_file_name} and {data_file_name}")

generate_shapes()

