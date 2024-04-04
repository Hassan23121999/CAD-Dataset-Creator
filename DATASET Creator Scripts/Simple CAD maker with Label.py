import cadquery as cq
import random
import os
import json
import xml.etree.ElementTree as ET
import pandas as pd

def create_pocket(box, length, width, height):
    pocket_shape = random.choice(['circle', 'rectangle'])
    depth = random.uniform(5, min(length, width, height) / 2)
    pocket_params = {'shape': pocket_shape, 'depth': depth}

    if pocket_shape == 'circle':
        diameter = random.uniform(5, min(length, width, height) / 2)
        box = box.faces(">Z").workplane().circle(diameter / 2).cutBlind(-depth)
        pocket_params['diameter'] = diameter
    elif pocket_shape == 'rectangle':
        pocket_length, pocket_width = random.uniform(5, length / 2), random.uniform(5, width / 2)
        box = box.faces(">Z").workplane().rect(pocket_length, pocket_width).cutBlind(-depth)
        pocket_params['length'] = pocket_length
        pocket_params['width'] = pocket_width

    return box, pocket_params

def create_random_box_with_selected_feature(selected_feature, length, width, height):
    box = cq.Workplane("XY").box(length, width, height)
    features_data = {}

    if selected_feature == 'hole':
        hole_diameter = random.uniform(5, min(length, width, height)/2)
        box = box.faces(">Z").workplane().hole(hole_diameter)
        features_data['hole'] = {'diameter': hole_diameter}

    elif selected_feature == 'fillet':
        fillet_radius = random.uniform(1, 10)
        try:
            box = box.edges().fillet(fillet_radius)
            features_data['fillet'] = {'radius': fillet_radius}
        except Exception as e:
            print(f"Failed to apply fillet with radius {fillet_radius}: {e}")

    elif selected_feature == 'chamfer':
        chamfer_size = random.uniform(1, 5)
        try:
            box = box.edges().chamfer(chamfer_size)
            features_data['chamfer'] = {'size': chamfer_size}
        except Exception as e:
            print(f"Failed to apply chamfer with size {chamfer_size}: {e}")

    elif selected_feature == 'pocket':
        box, pocket_params = create_pocket(box, length, width, height)
        features_data['pocket'] = pocket_params

    return box, features_data

def create_label_data(features_data):
    label_data = {}
    for feature, params in features_data.items():
        label_data[feature] = params
    return label_data

def save_label_file(label_data, file_path, file_format):
    if file_format == 'json':
        with open(file_path, 'w') as file:
            json.dump(label_data, file, indent=4)
    elif file_format == 'xml':
        root = ET.Element("PartFeatures")
        for feature, params in label_data.items():
            feature_element = ET.SubElement(root, feature)
            for param, value in params.items():
                param_element = ET.SubElement(feature_element, param)
                param_element.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(file_path)
    elif file_format == 'excel':
        df = pd.DataFrame({k: [v] for k, v in label_data.items()})
        df.to_excel(file_path, index=False)

def main():
    num_parts = int(input("How many parts do you want to create? "))
    file_format = input("Choose label file format (json/xml/excel): ").lower()
    selected_feature = input("Choose a feature to apply (hole/fillet/chamfer/pocket/etc): ").lower()

    dir_path = r"C:\Users\Muhammad Hassan\Desktop\fraunhofer\Test Datasets\Simple Shape Datasets\Class 4 Pocket"

    for i in range(num_parts):
        length, width, height = random.uniform(20, 100), random.uniform(20, 100), random.uniform(20, 100)
        box, features_data = create_random_box_with_selected_feature(selected_feature, length, width, height)

        file_path = os.path.join(dir_path, f'boxfraunhofer_part_{i+1}.step')
        box.val().exportStep(file_path)
        print(f'Part {i+1} saved to {file_path}')

        stl_file_path = os.path.join(dir_path, f'boxfraunhofer_part_{i+1}.stl')
        box.val().exportStl(stl_file_path)
        print(f'STL file for part {i+1} saved to {stl_file_path}')

        label_data = create_label_data(features_data)
        label_file_path = os.path.join(dir_path, f'boxfraunhofer_part_{i+1}.{file_format}')
        save_label_file(label_data, label_file_path, file_format)
        print(f'Label for part {i+1} saved to {label_file_path}')

if __name__ == "__main__":
    main()
