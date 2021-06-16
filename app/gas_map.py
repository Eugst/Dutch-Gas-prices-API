import requests
import simplekml
r = requests.get(url='https://tankservice.app-it-up.com/Tankservice/v1/places?fmt=web')
# print(r.json())

# dict((item['id'], item) for item in json_data['data'])

count = 0
for item in r.json():
    print(count)
    if count % 2000 == 0:
        if count != 0:
            kml.save("gas_stations_"+ str(count) +".kml")
        kml = simplekml.Kml()
    # print(item)
    kml.newpoint(
        name = str(item['id']),
        description = item['brand'] + item['name'],
        coords = [(item['lng']/1000000, item['lat']/1000000)]
    )
    count += 1
kml.save("gas_stations_"+ str(count) +".kml")
