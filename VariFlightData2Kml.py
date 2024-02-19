import csv
import json
import os
import simplekml


def get_file_list(path):
    """获取需要转换的文件列表"""
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.csv' or os.path.splitext(file)[1] == '.json':
                file_list.append(path + '/' + file)
    while file_list:
        read_file(file_list)
    else:
        print("the file is not exist!")


# def read_csv(csv_file_list):
#     for csv_file in csv_file_list:
#         try:
#             with open(csv_file) as f:
#                 csv_reader = csv.DictReader(f)
#                 coords = create_coordinates(csv_reader)
#         except FileNotFoundError:
#             print("the file does not exist")
#         create_kml(coords, csv_file)
#
#
# def read_json(json_file_list):
#     for json_file in json_file_list:
#         try:
#             with open(json_file) as f:
#                 json_reader = json.load(f)
#                 coords = create_coordinates(json_reader)
#         except FileNotFoundError:
#             print("the file does not exist")
#         create_kml(coords, json_file)


def read_file(file_list):
    """根据文件类型分别读取文件，获取坐标"""
    for file in file_list:
        # coordinates = []
        # if os.path.splitext(file)[1] == '.csv':
        #     try:
        #         with open(file) as f:
        #             coordinates = create_coordinates(csv.DictReader(f))
        #     except FileNotFoundError:
        #         print("the file does not exist")
        # elif os.path.splitext(file)[1] == '.json':
        #     try:
        #         with open(file) as f:
        #             coordinates = create_coordinates(json.load(f))
        #     except FileNotFoundError:
        #         print("the file does not exist")
        # create_kml(coordinates, file)
        coordinates = []
        try:
            with open(file) as f:
                if os.path.splitext(file)[1] == '.csv':
                    coordinates = create_coordinates(csv.DictReader(f))
                else:
                    coordinates = create_coordinates(json.load(f))
        except:
            print("the file does not exist")
        create_kml(coordinates, file)



def create_coordinates(data):
    """每个文件分别创建坐标列表"""
    longitude, latitude, coordinates = [], [], []
    for line in data:
        '''json中是longitude，csv中表头为首字母大写：Longitude，通过判断区分两种，后续尝试修改csv表头，统一两种方法'''
        if 'longitude' in line and 'latitude' in line:
            longitude.append(line['longitude'])
            latitude.append(line['latitude'])
        else:
            longitude.append(line['Longitude'])
            latitude.append(line['Latitude'])
        coordinates = list(zip(longitude, latitude))
    return coordinates


def create_kml(coordinates, file_list):
    """根据坐标list生成kml线段文件"""
    # Create the KML document
    kml = simplekml.Kml(name="Tracks", open=1)
    doc = kml.newdocument(name='GPS device')

    # Create a folder
    fol = doc.newfolder(name='Tracks')

    # Create a new track in the folder
    trk = fol.newgxtrack()

    # Add all the information to the track
    trk.newgxcoord(coordinates)  # Ditto

    kml_file_name = os.path.splitext(file_list)[0] + '.kml'
    kml.save(kml_file_name)


def start():
    file_path = os.getcwd()
    get_file_list(file_path)


if __name__ == '__main__':
    start()
