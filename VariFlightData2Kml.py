import os

import simplekml
import csv


def get_csv_list(path):
    L = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.csv':
                L.append(path + '/' + file)
        if len(L) == 0:
            print(
                path + '\nThere is no csv file,Please check out!')
        return L


def read_a_csv(csv_file):
    try:
        with open(csv_file) as f:
            csv_reader = csv.DictReader(f)
            longitude, latitude, coords = [], [], []
            for line in csv_reader:
                longitude.append(line["Longitude"])
                latitude.append(line["Latitude"])
                coords = list(zip(longitude, latitude))
    except FileNotFoundError:
        print("the file does not exist")
    create_a_kml(coords, csv_file)


def create_a_kml(coord, csv_file):
    # Create the KML document
    kml = simplekml.Kml(name="Tracks", open=1)
    doc = kml.newdocument(name='GPS device')

    # Create a folder
    fol = doc.newfolder(name='Tracks')

    # Create a new track in the folder
    trk = fol.newgxtrack()

    # Add all the information to the track
    trk.newgxcoord(coord)  # Ditto
    kml_file_name = csv_file[:-3]+'kml'
    kml.save(kml_file_name)


def start():
    csv_path = os.getcwd()
    json_path = os
    csv_list = get_csv_list(csv_path)
    for csv_file in csv_list:
        read_a_csv(csv_file)


if __name__ == '__main__':
    start()
