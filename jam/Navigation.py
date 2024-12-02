import flet as ft
import json
import os
import requests
from datetime import datetime, timedelta
from typing import Dict

# JSON ファイルのパス
json_path = os.path.join(os.path.dirname(__file__), 'data.json')

# JSON ファイルを読み込む
try:
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"JSON ファイル '{json_path}' が見つかりません。")

# 地域コードをキーにして地域名を取得できるようにする
area_cache: Dict[str, Dict] = {}

def format_date(date_str: str) -> str:
# 日付文字列を受け取って、日本語の日付文字列に変換して返す
    date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return date.strftime("%Y年%m月%d日")

def get_weather_text(code: str) -> str:
# 天気コードに対応する天気を返す
    weather_codes = {
        "100": "晴れ",
        "101": "晴れ時々曇り",
        "102": "晴れ時々雨",
        "200": "曇り",
        "201": "曇り時々晴れ",
        "202": "曇り時々雨",
        "218": "曇り時々雪",
        "270": "雪時々曇り",
        "300": "雨",
        "400": "雪",
        "500": "雷雨",
        "413": "雪のち雨",
        "206": "雨時々曇り",
        "111": "雨時々晴れ",
        "112": "雨時々雪",
        "211": "雪時々晴れ",
        "206": "雨時々曇り",
        "212": "雪時々曇り",
        "313": "雪のち雨",
        "314": "雨のち雪",
        "203": "曇り時々雪",
        "302": "雪",
        "114": "雪時々晴れ",
    }
    return weather_codes.get(code, f"不明な天気 (コード: {code})")

def get_weather_text(code: str) -> str:
# 天気コードに対応する天気を返す
    weather_codes = {
        "100": "晴れ",
        "101": "晴れ時々曇り",
        "102": "晴れ時々雨",
        "200": "曇り",
        "201": "曇り時々晴れ",
        "202": "曇り時々雨",
        "218": "曇り時々雪",
        "270": "雪時々曇り",
        "300": "雨",
        "400": "雪",
        "500": "雷雨",
        "413": "雪のち雨",
        "206": "雨時々曇り",
        "111": "雨時々晴れ",
        "112": "雨時々雪",
        "211": "雪時々晴れ",
        "206": "雨時々曇り",
        "212": "雪時々曇り",
        "313": "雪のち雨",
        "314": "雨のち雪",
        "203": "曇り時々雪",
        "302": "雪",
        "114": "雪時々晴れ",
    }
    return weather_codes.get(code, f"不明な天気 (コード: {code})")

def get_weather_icon(code: str) -> str:
# 天気コードに対応する絵文字を返す
    weather_icons = {
        "100": "☀️",  # 晴れ
        "101": "🌤️",  # 晴れ時々曇り
        "102": "🌦️",  # 晴れ時々雨
        "200": "☁️",  # 曇り
        "300": "🌧️",  # 雨
        "400": "❄️",  # 雪
        "500": "⛈️",  # 雷雨
        "413": "❄️→🌧️",  # 雪のち雨
        "314": "🌧️→❄️",  # 雨のち雪
        "201": "🌤️",
        "202": "☁️🌧️",
        "218": "☁️❄️",
        "270": "❄️☁️",
        "206": "🌧️☁️",
        "111": "🌧️☀️",
        "112": "🌧️❄️",
        "211": "❄️☀️",
        "212": "❄️☁️",
        "313": "❄️🌧️",
        "203": "☁️❄️",
        "302": "❄️",
        "114": "❄️☀️",



    }
    # 聞いたことも無い天気の場合は❓を返す
    return weather_icons.get(code, "❓")

def main(page: ft.Page):
    page.title = "地域選択と天気予報表示"
    page.theme_mode = "light"

    # 選択情報の表示
    selected_item = ft.Text("天気予報", size=20)
    selected_index = None  # 選択されたアイテムのインデックス
    forecast_view = ft.Column(spacing=10, expand=True)

    # 地域リスト
    region_list_view = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
    )

    # プログレスバーの定義付け
    progress_bar = ft.ProgressBar(visible=False)

    # 天気予報表示
    forecast_view = ft.Column(
        expand=True,
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )


    def fetch_data(url: str) -> Dict:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            show_error(f"データ取得エラー: {str(e)}")
            return {}
        
    def load_region_list():
        try:
            progress_bar.visible = True
            page.update()

            data = fetch_data("http://www.jma.go.jp/bosai/common/const/area.json")
            if "offices" in data:
                area_cache.update(data["offices"])
                update_region_menu()
            else:
                show_error("地域データの形式が予期したものと異なります。")
        except Exception as e:
                show_error(f"地域データの読み込みに失敗しました: {str(e)}")
        finally:
            progress_bar.visible = False
    