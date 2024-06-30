import csv
import requests
from bs4 import BeautifulSoup
import re

# WebページのURL
url = "https://gosenzo.net/yamajiro/%e6%94%bb%e5%9f%8e%e4%b8%80%e8%a6%a7/"
output_csv_path = "castles-list.csv"

# 除外するURLリスト
exclude_urls = [
    "https://gosenzo.net/yamajiro/",
    "https://gosenzo.net/yamajiro/%e3%83%97%e3%83%ad%e3%83%95%e3%82%a3%e3%83%bc%e3%83%ab/",
    "https://gosenzo.net/yamajiro/%e3%83%97%e3%83%a9%e3%82%a4%e3%83%90%e3%82%b7%e3%83%bc%e3%83%9d%e3%83%aa%e3%82%b7%e3%83%bc%e3%83%bb%e5%85%8d%e8%b2%ac%e4%ba%8b%e9%a0%85/",
    "https://gosenzo.net/yamajiro/%e3%81%8a%e5%95%8f%e3%81%84%e5%90%88%e3%82%8f%e3%81%9b/",
    "//b.hatena.ne.jp/entry/https://gosenzo.net/yamajiro/%e6%94%bb%e5%9f%8e%e4%b8%80%e8%a6%a7/",
    "https://twitter.com/share",
    "https://getpocket.com/save",
    "https://gosenzo.net/yamajiro/",
    "https://gosenzo.net/yamajiro/%e6%94%bb%e5%9f%8e%e4%b8%80%e8%a6%a7/",
    "https://gosenzo.net/yamajiro/%e3%80%90%e5%ba%83%e5%b3%b6%e7%9c%8c%e4%b8%89%e6%ac%a1%e5%b8%82%e5%a4%aa%e9%83%8e%e4%b8%b8%e3%80%91%e4%b8%ad%e4%b8%96%e3%81%ae%e5%9c%b0%e4%be%8d%e3%81%ab%e3%81%a4%e3%81%84%e3%81%a6/",
    "https://gosenzo.net/yamajiro/%e3%80%90%e5%ba%83%e5%b3%b6%e5%b8%82%e8%a5%bf%e5%8c%ba%e3%80%81%e5%ae%89%e4%bd%90%e5%8c%97%e5%8c%ba%e3%80%91%e4%b8%ad%e4%b8%96%e8%bf%91%e4%b8%96%e3%81%ae%e5%b7%b1%e6%96%90%e6%b0%8f%e3%81%ab%e3%81%a4/",
    "https://gosenzo.net/yamajiro/%e3%80%90%e5%ba%83%e5%b3%b6%e7%9c%8c%e5%ba%84%e5%8e%9f%e5%b8%82%e6%9d%b1%e5%9f%8e%e7%94%ba%e5%b0%8f%e5%a5%b4%e5%8f%af%e3%80%91%e4%b8%ad%e4%b8%96%e5%b0%8f%e5%a5%b4%e5%8f%af%e6%b0%8f%e3%81%ab%e3%81%a4/",
    "https://gosenzo.net/yamajiro/%e3%80%90%e5%ba%83%e5%b3%b6%e5%b8%82%e6%9d%b1%e5%8c%ba%e6%88%b8%e5%9d%82%e3%80%91%e4%b8%ad%e4%b8%96%e6%88%b8%e5%9d%82%e6%b0%8f%e3%81%ab%e3%81%a4%e3%81%84%e3%81%a6/",
    "https://gosenzo.net/yamajiro/%e3%80%90%e5%ba%83%e5%b3%b6%e5%b8%82%e7%99%bd%e6%9c%a8%e7%94%ba%e3%80%91%e4%b8%ad%e4%b8%96%e7%a7%8b%e5%b1%b1%e6%b0%8f%e3%81%ab%e3%81%a4%e3%81%84%e3%81%a6/",
    "https://gosenzo.net/yamajiro/%e5%9f%8e%e3%81%ab%e9%96%a2%e3%82%8f%e3%82%8b%e3%82%b5%e3%82%a4%e3%83%88/",
    "https://gosenzo.net/yamajiro/%e3%83%97%e3%83%ad%e3%83%95%e3%82%a3%e3%83%bc%e3%83%ab/",
    "https://gosenzo.net/yamajiro/%e3%81%8a%e5%95%8f%e3%81%84%e5%90%88%e3%82%8f%e3%81%9b/",
    "https://gosenzo.net/yamajiro/%e3%83%97%e3%83%a9%e3%82%a4%e3%83%90%e3%82%b7%e3%83%bc%e3%83%9d%e3%83%aa%e3%82%b7%e3%83%bc%e3%83%bb%e5%85%8d%e8%b2%ac%e4%ba%8b%e9%a0%85/",
    "https://gosenzo.net/yamajiro",
    "https://gosenzo.net/yamajiro",
    "https://gosenzo.net/yamajiro",
    "https://gosenzo.net/yamajiro/%e6%94%bb%e5%9f%8e%e4%b8%80%e8%a6%a7/",
    "https://gosenzo.net/yamajiro/%e3%80%90%e5%ba%83%e5%b3%b6%e5%b8%82%e7%99%bd%e6%9c%a8%e7%94%ba%e3%80%91%e4%b8%ad%e4%b8%96%e7%a7%8b%e5%b1%b1%e6%b0%8f%e3%81%ab%e3%81%a4%e3%81%84%e3%81%a6/",
    "https://gosenzo.net/yamajiro/%e3%80%90%e5%ba%83%e5%b3%b6%e5%b8%82%e6%9d%b1%e5%8c%ba%e6%88%b8%e5%9d%82%e3%80%91%e4%b8%ad%e4%b8%96%e6%88%b8%e5%9d%82%e6%b0%8f%e3%81%ab%e3%81%a4%e3%81%84%e3%81%a6/",
    "https://gosenzo.net/yamajiro/2021/01/10/%e3%80%90%e5%ba%83%e5%b3%b6%e7%9c%8c%e3%80%91%e8%83%bd%e7%be%8e%e5%9f%8e%e3%80%90%e6%b1%9f%e7%94%b0%e5%b3%b6%e5%b8%82%e5%a4%a7%e6%9f%bf%e7%94%ba%e5%a4%a7%e5%8e%9f%e3%80%91/",
    "https://gosenzo.net/yamajiro/2021/09/26/%e3%80%90%e5%85%b5%e5%ba%ab%e7%9c%8c%e3%80%91%e9%a6%99%e5%b1%b1%e5%9f%8e%e3%80%90%e3%81%9f%e3%81%a4%e3%81%ae%e5%b8%82%e6%96%b0%e5%ae%ae%e7%94%ba%e9%a6%99%e5%b1%b1%e3%80%91/",
    "https://twitter.com/yamajirokoujyou?ref_src=twsrc%5Etfw",
    "https://gosenzo.net/yamajiro/",
]

# コメントを含むURLパターンの正規表現
comment_pattern = re.compile(r'#comment-\d+$')

# HTMLコンテンツを取得
response = requests.get(url)
response.encoding = 'utf-8'
html_content = response.text

# HTMLコンテンツを解析
soup = BeautifulSoup(html_content, 'html.parser')

# 城名と対応するURLを抽出
castles = []
for link in soup.find_all('a', href=True):  # href属性が存在するaタグのみを対象
    url = link['href'].strip()

    # URLが除外リストに完全一致するか、#で始まるか、コメントパターンに一致する場合はスキップ
    if url in exclude_urls or url.startswith("#") or comment_pattern.search(url):
        continue

    castle_name = link.get_text(strip=True)
    if castle_name:  # 空でない場合のみ追加
        castles.append((castle_name, url))

# 抽出したデータをCSVファイルに書き込み
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["城名", "URL"])
    writer.writerows(castles)

print(f"城のデータが '{output_csv_path}' に正常に保存されました")
