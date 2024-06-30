import csv
import requests
from bs4 import BeautifulSoup

# URLから城データと座標を取得する関数
def fetch_castle_data(url):
    castle_data_list = []
    try:
        response = requests.get(url)
        response.raise_for_status()  # レスポンスエラーを確認
        soup = BeautifulSoup(response.text, 'html.parser')

        # 初期値を空文字で設定
        castle_name = ""
        alias = ""
        construction_year = ""
        lords = ""
        location = ""
        latitude = ""
        longitude = ""

        # 各pタグから必要なデータを抽出
        for p_tag in soup.find_all('p'):
            text = p_tag.text
            if '城名：' in text:
                if castle_name:  # すでに城名がセットされていれば、新しい城の情報開始前に現在の城をリストに追加
                    castle_data_list.append((castle_name, alias, construction_year, lords, location, latitude, longitude))
                    # 新しい城のデータのために変数をリセット
                    alias = ""
                    construction_year = ""
                    lords = ""
                    location = ""
                    latitude = ""
                    longitude = ""
                castle_name = text.split('：')[1].strip()
            elif '別名：' in text:
                alias = text.split('：')[1].strip()
            elif '築城年：' in text:
                construction_year = text.split('：')[1].strip()
            elif '城主：' in text:
                lords = text.split('：')[1].strip()
            elif '場所：' in text:
                location = text.split('：')[1].strip()
            elif '北緯:東経' in text or '北緯東経' in text:
                coordinates_text = text.split('：')[1].strip()
                first_coordinate = coordinates_text.split('　')[0]  # 全角スペースで分割
                for separator in ['/', '，', ',']:
                    parts = first_coordinate.split(separator)
                    if len(parts) == 2:
                        latitude, longitude = parts[0].strip(), parts[1].strip()
                        break

        # 最後の城のデータを追加
        if castle_name:
            castle_data_list.append((castle_name, alias, construction_year, lords, location, latitude, longitude))

    except requests.RequestException as e:
        print(f"URL {url} からのデータ取得中にエラーが発生しました: {e}")
    return castle_data_list

# CSVファイルを読み込む
with open('castles-list.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # ヘッダー行をスキップ
    rows = list(reader)

# 各行に城データと座標を追加
updated_rows = []
count = 0
for row in rows:
    if len(row) > 1:  # URLが存在する行のみ処理
        original_castle_name, url = row[0], row[1]
        castle_data = fetch_castle_data(url)
        for data in castle_data:
            castle_name, alias, construction_year, lords, location, latitude, longitude = data
            updated_rows.append([original_castle_name, url, castle_name, alias, construction_year, lords, location, latitude, longitude])
            count += 1
            print(f"{count}件目: {castle_name}を処理中...")

# 更新されたデータをCSVに書き出す
with open('castles-data.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["元の城名", "URL", "城名", "別名", "築城年", "城主", "場所", "Latitude", "Longitude"])
    writer.writerows(updated_rows)

print(f"処理が完了しました。全{count}件の城のデータを追加して 'castles-data.csv' に保存しました。")
