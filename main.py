import flet as ft
import datetime

def main(page: ft.Page):
    page.title = "I-Manager Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    
    # Функция для создания карточки задачи в расписании
    def tech_card(time, activity, venue, duties, tech_name, color):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(time, weight="bold", size=16, color=ft.colors.WHITE),
                    ft.Text(tech_name, weight="bold", color=color),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(f"📍 {venue}", size=12, color=ft.colors.GREY_400),
                ft.Text(activity, size=18, weight="w500"),
                ft.Text(f"🛠 {duties}", size=14, italic=True, color=ft.colors.BLUE_200),
            ], spacing=5),
            padding=15,
            border_radius=10,
            border=ft.border.all(1, color),
            margin=ft.margin.only(bottom=10)
        )

    # Вкладка Расписания (на основе твоего скрина)
    schedule_view = ft.Column([
        ft.Text("Stage Team Schedule", size=24, weight="bold"),
        ft.Divider(),
        ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Oleksandar", content=ft.Column([
                    tech_card("15:45", "Port Talk", "Star Theater", "Setup & Run", "Oleksandar", ft.colors.BLUE),
                    tech_card("19:15", "Duets", "Star Theater", "Setup & Run", "Oleksandar", ft.colors.BLUE),
                ], scroll=ft.ScrollMode.ADAPTIVE)),
                ft.Tab(text="Joson", content=ft.Column([
                    tech_card("17:00", "Guitarist", "Explorer's Lounge", "Setup & Strike", "Joson", ft.colors.RED),
                    tech_card("19:15", "Duets", "Star Theater", "Setup & Run", "Joson", ft.colors.RED),
                ], scroll=ft.ScrollMode.ADAPTIVE)),
                ft.Tab(text="Others", content=ft.Column([
                    ft.Text("Important Phones:", weight="bold"),
                    ft.ListTile(leading=ft.Icon(ft.icons.PHONE), title=ft.Text("Stage Manager: 2387")),
                    ft.ListTile(leading=ft.Icon(ft.icons.PHONE), title=ft.Text("Sound Tech: 2193")),
                    ft.ListTile(leading=ft.Icon(ft.icons.PHONE), title=ft.Text("Light Tech: 2192")),
                ], scroll=ft.ScrollMode.ADAPTIVE)),
            ],
            expand=1
        )
    ], visible=False)

    # Вкладка Live (Твой таймер)
    live_view = ft.Column([
        ft.Text("Live Production", size=24, weight="bold"),
        ft.Container(
            content=ft.Text("00:00:00", size=60, weight="bold", color=ft.colors.GREEN),
            alignment=ft.alignment.center,
            height=200,
            border_radius=20,
            bgcolor=ft.colors.BLACK38
        ),
        ft.Text("Current Task: Port Talk", size=20),
        ft.ProgressBar(value=0.5, color="green")
    ], visible=True)

    # Навигация
    def nav_change(e):
        index = e.control.selected_index
        live_view.visible = (index == 0)
        schedule_view.visible = (index == 1)
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.PLAY_CIRCLE_OUTLINE, label="Live"),
            ft.NavigationDestination(icon=ft.icons.CHRONO_OUTLINED, label="Schedule"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
        ],
        on_change=nav_change
    )

    page.add(live_view, schedule_view)

ft.app(target=main)
