# リポジトリ概要
このリポジトリは、[山城攻城記様](https://x.com/yamajirokoujyou)が[公開されているサイト](https://gosenzo.net/yamajiro/)から城に関するデータを収集し、加工してGeoJSON形式で提供する自動化プロセスを実装しています。
データは公開されたウェブページからスクレイピングされ、整形された後、地理的データ形式に変換されます。

# 処理フロー
- **下記の処理を毎週月曜日午前6時（JST）に自動実行します。**
1. データ収集: 指定されたウェブページから城に関するデータを収集します。
2. データ加工: 収集したデータをCSV形式で保存し、後処理を行います。
3. GeoJSON生成: 加工されたデータからGeoJSONファイルを生成します。

# データのライセンス
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja)
