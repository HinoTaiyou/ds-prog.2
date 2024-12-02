import flet as ft
import json
import os
import requests
from datetime import datetime, timedelta
from typing import Dict

# JSON ファイルのパス
json_path = os.path.join(os.path.dirname(__file__), 'region.json')

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