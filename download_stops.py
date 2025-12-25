import json
import requests


#Сервер overpass + запрос
OVERPASS_URL = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"


QUERY = r"""
[out:json][timeout:120];
(
  node["highway"="bus_stop"](59.8133, 30.0648,60.0751, 30.5503);
  node["public_transport"="platform"](59.8133, 30.0648,60.0751, 30.5503);
  node["public_transport"="stop_position"](59.8133, 30.0648,60.0751, 30.5503);
);
out body;
"""


def main():
    #Отправка запроса
    r = requests.post(OVERPASS_URL, data={"data": QUERY}, timeout=180)
    r.raise_for_status()
    osm = r.json()

    #Формирование списка для geoJSON и рассмотрение только точек
    features = []
    for el in osm.get("elements", []):
        if el["type"] != "node":
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [el["lon"], el["lat"]]
            },
            "properties": {
                "osm_id": el["id"],
                "name": el.get("tags", {}).get("name"),
                "highway": el.get("tags", {}).get("highway"),
                "public_transport": el.get("tags", {}).get("public_transport")
            }
        })

    #Создание FeatureCollection и сохранение сырых данных
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open("data/stops.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)

    print(f"Сохранено {len(features)} остановок")

if __name__ == "__main__":
    main()
