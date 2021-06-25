import requests
import simplekml
from pathlib import Path
import shutil


def gas_map():
    r = requests.get(url='https://tankservice.app-it-up.com/Tankservice/v1/places?fmt=web')
    count = 0
    dir_name = 'cache/maps/'
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    for item in r.json():
        print(count)
        if count % 2000 == 0:
            if count != 0:
                kml.save(dir_name + 'gas_stations_'+ str(count) +'.kml')
            kml = simplekml.Kml()
        kml.newpoint(
            name = 'Id: ' + str(item['id']),
            description = item['brand'] + ' ' + item['name'],
            coords = [(item['lng']/1000000, item['lat']/1000000)]
        )
        count += 1
    kml.save(dir_name + 'gas_stations_' + str(count) + '.kml')
    archive_name = dir_name + 'archive.zip'
    shutil.make_archive(archive_name, 'zip', dir_name)
    return archive_name
