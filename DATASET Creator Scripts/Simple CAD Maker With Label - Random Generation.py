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

def create_random_box():
    length, width, height = random.uniform(20, 100), random.uniform(20, 100), random.uniform(20, 100)
    box = cq.Workplane("XY").box(length, width, height)

    features = ['hole', 'fillet', 'chamfer', 'cutout', 'revolved', 'slot', 'extruded', 'pocket']
    chosen_features = random.sample(features, k=random.randint(1, 3))
    features_data = {'dimensions': {'length': length, 'width': width, 'height': height}}

    for feature in chosen_features:
        if feature == 'hole':
            hole_diameter = random.uniform(5, min(length, width, height)/2)
            box = box.faces(">Z").workplane().hole(hole_diameter)
            features_data['hole'] = {'diameter': hole_diameter}

        elif feature == 'fillet':
            fillet_radius = random.uniform(1, 10)
            try:
                box = box.edges().fillet(fillet_radius)
                features_data['fillet'] = {'radius': fillet_radius}
            except Exception as e:
                print(f"Failed to apply fillet with radius {fillet_radius}: {e}")

        elif feature == 'chamfer':
            chamfer_size = random.uniform(1, 5)
            try:
                box = box.edges().chamfer(chamfer_size)
                features_data['chamfer'] = {'size': chamfer_size}
            except Exception as e:
                print(f"Failed to apply chamfer with size {chamfer_size}: {e}")

        elif feature == 'cutout':
            cutout_length, cutout_width = random.uniform(5, length/2), random.uniform(5, width/2)
            box = box.faces(">Z").workplane().rect(cutout_length, cutout_width).cutThruAll()
            features_data['cutout'] = {'length': cutout_length, 'width': cutout_width}

        elif feature == 'revolved':
            try:
                profile_width, profile_height = random.uniform(5, 10), random.uniform(5, height/2)
                box = box.faces(">Z").workplane().rect(profile_width, profile_height).revolve()
                features_data['revolved'] = {'profile_width': profile_width, 'profile_height': profile_height}
            except Exception as e:
                print(f"Failed to apply revolve feature: {e}")

        elif feature == 'slot':
            slot_length, slot_width = random.uniform(5, length/2), random.uniform(1, 3)
            box = box.faces(">Z").workplane().slot2D(slot_length, slot_width).cutThruAll()
            features_data['slot'] = {'length': slot_length, 'width': slot_width}

        elif feature == 'extruded':
            extrude_length, extrude_width = random.uniform(5, length/2), random.uniform(5, width/2)
            extrusion_height = random.uniform(1, 5)
            box = box.faces(">Z").workplane().rect(extrude_length, extrude_width).extrude(extrusion_height)
            features_data['extruded'] = {'length': extrude_length, 'width': extrude_width, 'height': extrusion_height}

        elif feature == 'pocket':
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

    dir_path = r"C:\Users\Muhammad Hassan\Desktop\fraunhofer\Test Datasets\Simple shape Dataset Random"

    for i in range(num_parts):
        random_box, features_data = create_random_box()

        file_path = os.path.join(dir_path, f'boxfraunhofer_part_{i+1}.step')
        random_box.val().exportStep(file_path)
        print(f'Part {i+1} saved to {file_path}')

        # STL file
        stl_file_path = os.path.join(dir_path, f'boxfraunhofer_part_{i+1}.stl')
        random_box.val().exportStl(stl_file_path)
        print(f'STL file for part {i+1} saved to {stl_file_path}')

        label_data = create_label_data(features_data)
        label_file_path = os.path.join(dir_path, f'boxfraunhofer_part_{i+1}.json')
        save_label_file(label_data, label_file_path, file_format)
        print(f'Label for part {i+1} saved to {label_file_path}')

if __name__ == "__main__":
    main()
