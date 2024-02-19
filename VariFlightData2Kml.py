import csv
import json
import os

import simplekml


def get_file_list(path):
    csv_list, json_list = [], []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.csv':
                csv_list.append(path + '/' + file)
            elif os.path.splitext(file)[1] == '.json':
                json_list.append(path + '/' + file)
        if len(csv_list) == 0 and len(json_list) == 0:
            print(path + '\nThere is no csv and json file,Please check out!')
        if len(csv_list) != 0:
            read_csv(csv_list)
        if len(json_list) != 0:
            read_json(json_list)


def read_csv(csv_file_list):
    for csv_file in csv_file_list:
        try:
            with open(csv_file) as f:
                csv_reader = csv.DictReader(f)
                coords = create_coordinates(csv_reader)
        except FileNotFoundError:
            print("the file does not exist")
        create_kml(coords, csv_file)


def read_json(json_file_list):
    for json_file in json_file_list:
        try:
            with open(json_file) as f:
                json_reader = json.load(f)
                coords = create_coordinates(json_reader)
        except FileNotFoundError:
            print("the file does not exist")
        create_kml(coords, json_file)


def create_coordinates(data):
    longitude, latitude, coords = [], [], []
    for line in data:
        if 'longitude' in line and 'latitude' in line:
            longitude.append(line['longitude'])
            latitude.append(line['latitude'])
        else:
            longitude.append(line['Longitude'])
            latitude.append(line['Latitude'])
        coords = list(zip(longitude, latitude))
    return coords


def create_kml(coord, file_list):
    # Create the KML document
    kml = simplekml.Kml(name="Tracks", open=1)
    doc = kml.newdocument(name='GPS device')

    # Create a folder
    fol = doc.newfolder(name='Tracks')

    # Create a new track in the folder
    trk = fol.newgxtrack()

    # Add all the information to the track
    trk.newgxcoord(coord)  # Ditto

    # kml_file_name = file_list[:-3] + 'kml'
    kml_file_name = file_list.split('.')[0]+'.kml'
    kml.save(kml_file_name)


def start():
    file_path = os.getcwd()
    get_file_list(file_path)


if __name__ == '__main__':
    start()
