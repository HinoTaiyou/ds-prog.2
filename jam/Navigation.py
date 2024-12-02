import flet as ft
import requests

def main(page: ft.Page):

    # JMAの地域データを取得
    url = "https://www.jma.go.jp/bosai/common/const/area.json"
    response = requests.get(url)
    area_data = response.json()

    # 地域データを抽出
    regions = [region['name'] for region in area_data]

    # Navigation Railを作成
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, label=region
            )
            for region in regions
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    # Body部分
    body_column = ft.Column([ft.Text("Please select a region.")], alignment=ft.MainAxisAlignment.START, expand=True)

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                body_column,
            ],
            expand=True,
        )
    )

ft.app(main)
