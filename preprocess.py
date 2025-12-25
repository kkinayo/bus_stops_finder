import json

INPUT_FILE = "data/stops.geojson"
OUTPUT_FILE = "data/stops_processed.geojson"

#Чтениие и извлечение geojson данных
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data.get("features", [])

processed = []
stats = {
    "total": 0,
    "with_name": 0,
    "bus": 0,
    "platform": 0,
    "unknown": 0
}

for f in features:
    props = f.get("properties", {})

    name = props.get("name")
    has_name = bool(name and name.strip())

    if props.get("highway") == "bus_stop":
        stop_type = "bus"
        stats["bus"] += 1
    elif props.get("public_transport") == "platform":
        stop_type = "platform"
        stats["platform"] += 1
    else:
        stop_type = "unknown"
        stats["unknown"] += 1

    if has_name:
        stats["with_name"] += 1

    stats["total"] += 1

    props["stop_type"] = stop_type
    props["has_name"] = has_name

    f["properties"] = props
    processed.append(f)

out = {
    "type": "FeatureCollection",
    "features": processed
}

#Сохранение обработанных данныaх
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("Предобработка завершена")
print("Всего остановок:", stats["total"])
print("С названием:", stats["with_name"])
print("Автобусные:", stats["bus"])
print("Платформы:", stats["platform"])
print("Неопределенные:", stats["unknown"])
