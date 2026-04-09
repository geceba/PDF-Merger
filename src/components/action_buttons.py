import customtkinter as ctk
from src.utils.constants import (
    COLOR_BLUE_PRIMARY, COLOR_BLUE_HOVER, 
    COLOR_GRAY_DARK, COLOR_GRAY_HOVER,
    COLOR_SLATE, COLOR_SLATE_HOVER,
    BTN_CORNER_RADIUS, BTN_HEIGHT
)

class ActionButtons(ctk.CTkFrame):
    def __init__(self, master, icons, commands):
        super().__init__(master, fg_color="transparent")

        base_config = {
            "compound": "right", 
            "corner_radius": BTN_CORNER_RADIUS, 
            "height": BTN_HEIGHT
        }

        ctk.CTkButton(self, text="Agregar", image=icons['add'], 
                      command=commands['add'], fg_color=COLOR_BLUE_PRIMARY, hover_color=COLOR_BLUE_HOVER, **base_config).grid(row=0, column=0, padx=5)
        ctk.CTkButton(self, text="Limpiar", image=icons['trash'], 
                      command=commands['clear'], fg_color=COLOR_GRAY_DARK, hover_color=COLOR_GRAY_HOVER, **base_config).grid(row=0, column=1, padx=5)
        ctk.CTkButton(self, text="Subir", image=icons['up'], 
                      command=commands['up'], fg_color=COLOR_SLATE, hover_color=COLOR_SLATE_HOVER, **base_config).grid(row=0, column=2, padx=5)
        ctk.CTkButton(self, text="Bajar", image=icons['down'], 
                      command=commands['down'], fg_color=COLOR_SLATE, hover_color=COLOR_SLATE_HOVER, **base_config).grid(row=0, column=3   , padx=5)
        