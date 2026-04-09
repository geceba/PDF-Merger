import customtkinter as ctk
import os
from src.utils.constants import COLOR_SELECTED_ITEM, COLOR_DANGER

class FileItem(ctk.CTkFrame):
    def __init__(self, master, path, index, is_selected, icon_pdf, on_select, on_delete):
        super().__init__(master)

        if is_selected:
            self.configure(fg_color=COLOR_SELECTED_ITEM)

        self.icon_label = ctk.CTkLabel(self, image=icon_pdf, text="", cursor="hand2")
        self.icon_label.pack(side="left", padx=10)

        name = os.path.basename(path)
        self.name_label = ctk.CTkLabel(self, text=name, cursor="hand2")
        self.name_label.pack(side="left", padx=5)

        self.btn_delete = ctk.CTkButton(
            self, 
            text="✕", 
            width=28, 
            height=28,
            fg_color="transparent",
            hover_color=COLOR_DANGER,
            text_color="#FFFFFF",
            corner_radius=6,
            command=lambda: on_delete(index)
        )

        self.btn_delete.pack(side="right", padx=10)

        self.bind("<Button-1>", lambda e: on_select(index))
        self.icon_label.bind("<Button-1>", lambda e: on_select(index))
        self.name_label.bind("<Button-1>", lambda e: on_select(index))