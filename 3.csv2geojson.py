import pandas as pd
import json

# CSVファイルを読み込む
csv_file_path = 'castles-data.csv'
data = pd.read_csv(csv_file_path)

# GeoJSONフォーマットでデータを構築
geojson = {
    "type": "FeatureCollection",
    "name": "castles",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": []
}

# NaNをNoneに変換
data = data.where(pd.notnull(data), None)

# データフレームの各行に対して処理
for idx, row in data.iterrows():
    feature = {
        "type": "Feature",
        "properties": {
            "城名": row['城名'],
            "別名": row['別名'],
            "築城年": row['築城年'],
            "城主": row['城主'],
            "場所": row['場所'],
            # "URL": row['URL']
        },
        "geometry": {
            "type": "Point",
            "coordinates": [row['Longitude'], row['Latitude']]
        }
    }
    # HTMLリンクを新たな属性として追加
    if row['URL']:
        feature['properties']['山城攻城記URL'] = f"<a href='{row['URL']}'>クリックして表示</a>"

    geojson['features'].append(feature)

# GeoJSONオブジェクトを文字列に変換
geojson_str = json.dumps(geojson, ensure_ascii=False, indent=2)

# GeoJSONファイルを保存
geojson_file_path = 'castles-data.geojson'
with open(geojson_file_path, 'w', encoding='utf-8') as file:
    file.write(geojson_str)

print("加工後のGeoJSONファイルが保存されました: ", geojson_file_path)
