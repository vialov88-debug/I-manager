import flet as ft

def main(page: ft.Page):
    page.title = "I-Manager Hyper Edition"
    # Светлая тема часто лучше прогружается на новых Xiaomi при первом запуске
    page.theme_mode = ft.ThemeMode.DARK 
    page.padding = 15
    page.window_resizable = True

    # Универсальная карточка задачи
    def task_item(time, task, place, tech, color):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(time, size=18, weight="bold"),
                    ft.Container(
                        content=ft.Text(tech, size=12, color=ft.colors.BLACK, weight="bold"),
                        bgcolor=color,
                        padding=ft.padding.all(5),
                        border_radius=5,
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(task, size=16, weight="w500"),
                ft.Text(f"📍 {place}", size=13, color=ft.colors.GREY_400),
            ], spacing=5),
            padding=12,
            bgcolor=ft.colors.GREY_900,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_800)
        )

    # Список контактов из таблицы
    phones_view = ft.Column([
        ft.Text("Deck Phones", size=22, weight="bold"),
        ft.ListTile(leading=ft.Icon(ft.icons.PHONE), title=ft.Text("Stage Manager"), subtitle=ft.Text("2387")),
        ft.ListTile(leading=ft.Icon(ft.icons.PHONE), title=ft.Text("Sound Tech"), subtitle=ft.Text("2193")),
        ft.ListTile(leading=ft.Icon(ft.icons.PHONE), title=ft.Text("Light Tech"), subtitle=ft.Text("2192")),
        ft.ListTile(leading=ft.Icon(ft.icons.PHONE), title=ft.Text("Video Tech"), subtitle=ft.Text("2194")),
        ft.ListTile(leading=ft.Icon(ft.icons.PHONE), title=ft.Text("General Tech"), subtitle=ft.Text("2197")),
    ], scroll=ft.ScrollMode.ALWAYS, visible=False)

    # Расписание
    schedule_view = ft.Column([
        ft.Text("Team Schedule", size=22, weight="bold"),
        ft.Tabs(
            selected_index=0,
            expand=1,
            tabs=[
                ft.Tab(text="Oleksandar", content=ft.Column([
                    task_item("15:45", "Port Talk", "Star Theater", "Oleksandar", ft.colors.BLUE_400),
                    task_item("19:15", "Duets", "Star Theater", "Oleksandar", ft.colors.BLUE_400),
                ], scroll=ft.ScrollMode.ALWAYS)),
                ft.Tab(text="Joson", content=ft.Column([
                    task_item("17:00", "Guitarist", "Explorer's Lounge", "Joson", ft.colors.RED_400),
                    task_item("19:15", "Duets", "Star Theater", "Joson", ft.colors.RED_400),
                ], scroll=ft.ScrollMode.ALWAYS)),
                ft.Tab(text="Alex", content=ft.Column([
                    task_item("15:45", "Guitarist", "Wintergarden", "Alex", ft.colors.PURPLE_400),
                    task_item("16:00", "The Dome", "Explorer's Lounge", "Alex", ft.colors.PURPLE_400),
                ], scroll=ft.ScrollMode.ALWAYS)),
                ft.Tab(text="Romeo/Darko", content=ft.Column([
                    task_item("18:00", "Guest Lecture", "Star Theater", "Romeo", ft.colors.ORANGE_400),
                    task_item("16:15", "Port Talk", "Star Theater", "Darko", ft.colors.DEEP_PURPLE_400),
                ], scroll=ft.ScrollMode.ALWAYS)),
            ]
        )
    ], expand=True, visible=True)

    def on_nav(e):
        idx = e.control.selected_index
        schedule_view.visible = (idx == 0)
        phones_view.visible = (idx == 1)
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.LIST_ALT, label="Schedule"),
            ft.NavigationDestination(icon=ft.icons.CONTACT_PHONE, label="Phones"),
        ],
        on_change=on_nav
    )

    page.add(schedule_view, phones_view)

# Запуск в режиме с оптимизацией под мобильные экраны
ft.app(target=main)
