import flet as ft
import datetime
import asyncio

class ShowManager:
    def __init__(self):
        self.show_name = "New Show"
        self.show_start_time = None
        self.last_song_duration = 0
        self.patch = []
        self.notes = ""

manager = ShowManager()

async def main(page: ft.Page):
    page.title = "Sound Engineer Organizer"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # --- UI ЭЛЕМЕНТЫ ТАЙМЕРА ---
    timer_display = ft.Text("00:00:00", size=70, weight="bold", color="white")
    status_display = ft.Text("IDLE", size=20, color="gray")
    
    # --- ФУНКЦИЯ ОБНОВЛЕНИЯ ТАЙМЕРА ---
    async def update_clock():
        while True:
            if manager.show_start_time:
                now = datetime.datetime.now()
                diff = manager.show_start_time - now
                total_sec = diff.total_seconds()

                if total_sec > 0:
                    # Режим PRE-SHOW
                    status_display.value = "PRE-SHOW"
                    timer_display.color = "green" if total_sec > 300 else "yellow"
                    
                    # Триггеры уведомлений (простая проверка секунд)
                    current_sec = int(total_sec)
                    if current_sec == 900: # 15 min
                        page.show_snack_bar(ft.SnackBar(ft.Text("MIC CHECK!"), open=True))
                    if current_sec == 600: # 10 min
                        page.show_snack_bar(ft.SnackBar(ft.Text("CALL THE CAST!"), open=True))
                    if current_sec == manager.last_song_duration:
                        page.show_snack_bar(ft.SnackBar(ft.Text("START LAST SONG!"), open=True))
                else:
                    # Режим SHOW (прямой отсчет)
                    status_display.value = "SHOW IN PROGRESS"
                    timer_display.color = "red"
                    diff = now - manager.show_start_time

                abs_sec = abs(int(diff.total_seconds()))
                h, m, s = abs_sec // 3600, (abs_sec % 3600) // 60, abs_sec % 60
                timer_display.value = f"{h:02d}:{m:02d}:{s:02d}"
            
            page.update()
            await asyncio.sleep(1)

    # --- ЭКРАН ПАТЧА ---
    patch_grid = ft.GridView(expand=True, runs_count=3, max_extent=150, spacing=10)
    
    def add_channel(e):
        ch_num = len(patch_grid.controls) + 1
        patch_grid.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"CH {ch_num}", size=12, weight="bold"),
                    ft.TextField(border=ft.InputBorder.UNDERLINE, text_size=14, dense=True)
                ]),
                bgcolor=ft.colors.SURFACE_VARIANT, border_radius=10, padding=10
            )
        )
        page.update()

    # --- ЭКРАН ЗАМЕТОК ---
    notes_field = ft.TextField(label="Show Notes", multiline=True, min_lines=10, expand=True)

    # --- НАВИГАЦИЯ ---
    def on_nav_change(e):
        idx = e.control.selected_index
        tab_show.visible = (idx == 0)
        tab_calendar.visible = (idx == 1)
        tab_patch.visible = (idx == 2)
        tab_notes.visible = (idx == 3)
        page.update()

    # Вьюхи
    tab_show = ft.Column([
        ft.Text(manager.show_name, size=25, weight="bold"),
        status_display, timer_display
    ], horizontal_alignment="center", visible=True)

    tab_calendar = ft.Column([
        ft.TextField(label="Show Name", id="name"),
        ft.TextField(label="Start Time (HH:MM)", hint_text="21:00"),
        ft.TextField(label="Last Song Duration (MM:SS)", hint_text="04:20"),
        ft.ElevatedButton("Set Show", on_click=lambda _: save_show_data(tab_calendar))
    ], visible=False)

    def save_show_data(col):
        try:
            name = col.controls[0].value
            t_str = col.controls[1].value
            ls_str = col.controls[2].value
            
            t = datetime.datetime.strptime(t_str, "%H:%M")
            manager.show_start_time = datetime.datetime.now().replace(hour=t.hour, minute=t.minute, second=0)
            manager.show_name = name
            
            m, s = map(int, ls_str.split(":"))
            manager.last_song_duration = m * 60 + s
            
            page.show_snack_bar(ft.SnackBar(ft.Text("Success! Mode Active."), open=True))
        except:
            page.show_snack_bar(ft.SnackBar(ft.Text("Error! Check formats."), open=True))

    tab_patch = ft.Column([
        ft.Row([ft.Text("Patch", size=20), ft.IconButton(ft.icons.ADD, on_click=add_channel)]),
        patch_grid
    ], visible=False, expand=True)

    tab_notes = ft.Column([notes_field], visible=False, expand=True)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.PLAY_ARROW, label="Live"),
            ft.NavigationDestination(icon=ft.icons.CALENDAR_TODAY, label="Plan"),
            ft.NavigationDestination(icon=ft.icons.CABLE, label="Patch"),
            ft.NavigationDestination(icon=ft.icons.NOTES, label="Notes"),
        ],
        on_change=on_nav_change
    )

    page.add(ft.Column([tab_show, tab_calendar, tab_patch, tab_notes], expand=True))
    await update_clock()

ft.app(target=main)