# -*- coding: utf-8 -*-


__author__ = 'shaw'

import xml.dom.minidom
from datetime import datetime


KML_FILE_PATH = 'FlightAware_CSZ9898_ZSOF_ZGSZ_20230327.kml'
IMPROVED_KML_FILE_PATH = 'improved_FlightAware_CSZ9898_ZSOF_ZGSZ_20230327.kml'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def handle_when(whens):
    len_whens = len(whens)
    improved_whens = []
    for index, value in enumerate(whens):
        str_current = value.firstChild.data
        dt_current = datetime.strptime(str_current, DATETIME_FORMAT)
        improved_whens.append(str_current)

        next_index = index + 1
        if next_index < len_whens:
            str_next = whens[next_index].firstChild.data
            dt_next = datetime.strptime(str_next, DATETIME_FORMAT)

            diff = dt_next - dt_current
            mid = dt_current + diff / 2
            str_mid = mid.strftime(DATETIME_FORMAT)
            improved_whens.append(str_mid)

    return improved_whens


def handle_gx_coord(gx_coords):
    len_gx_coords = len(gx_coords)
    improved_gx_coords = []

    for index, value in enumerate(gx_coords):
        str_current = value.firstChild.data
        list_current = str_current.split(' ')

        longitude = float(list_current[0])
        latitude = float(list_current[1])
        altitude = int(list_current[2])

        improved_gx_coords.append(str_current)

        next_index = index + 1
        if next_index < len_gx_coords:
            str_next = gx_coords[next_index].firstChild.data
            list_next = str_next.split(' ')

            longitude_next = float(list_next[0])
            latitude_next = float(list_next[1])
            altitude_next = int(list_next[2])

            longitude_mid = (longitude_next + longitude) / 2
            latitude_mid = (latitude_next + latitude) / 2
            altitude_mid = int((altitude_next + altitude) / 2)

            str_mid = '%.5f %.5f %s' % (longitude_mid, latitude_mid, altitude_mid)
            improved_gx_coords.append(str_mid)

    return improved_gx_coords


if __name__ == '__main__':
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(KML_FILE_PATH)
    collection = DOMTree.documentElement

    placemark = collection.getElementsByTagName("Placemark")[2]
    gx_track = placemark.getElementsByTagName('gx:Track')[0]

    whens = gx_track.getElementsByTagName('when')
    improved_whens = handle_when(whens)
    print('len improved_whens = ' + str(len(improved_whens)))

    gx_coords = gx_track.getElementsByTagName('gx:coord')
    improved_gx_coords = handle_gx_coord(gx_coords)
    print('len improved_gx_coords = ' + str(len(improved_gx_coords)))

    kml_file = open(KML_FILE_PATH, mode='r', encoding='utf-8')
    kml_file_lines = kml_file.readlines()
    kml_file.close()

    improved_kml_file = open(IMPROVED_KML_FILE_PATH, mode='w+', encoding='utf-8')
    first_when = True
    first_gx_coord = True
    for line in kml_file_lines:
        if '<when>' in line:
            if first_when:
                for when in improved_whens:
                    improved_kml_file.writelines('            <when>%s</when>\n' % when)
                first_when = False
        elif '<gx:coord>' in line:
            if first_gx_coord:
                for gx_coord in improved_gx_coords:
                    improved_kml_file.writelines('            <gx:coord>%s</gx:coord>\n' % gx_coord)
                first_gx_coord = False
        else:
            improved_kml_file.writelines(line)
    improved_kml_file.close()
