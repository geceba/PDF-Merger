import customtkinter as ctk
from tkinterdnd2 import DND_FILES
from src.utils.constants import COLOR_BG_LIST, COLOR_TEXT_SECONDARY
from src.utils.i18n import TEXTS
from .file_item import FileItem

class FileListContainer(ctk.CTkFrame):
    def __init__(self, master, icons, on_drop_callback, on_select, on_delete):
        super().__init__(master, fg_color=COLOR_BG_LIST, corner_radius=12)

        self.icons = icons
        self.on_select = on_select
        self.on_delete = on_delete

        self.list_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", scrollbar_button_color="#333333"
        )
        self.list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.empty_icon = ctk.CTkLabel(self, text="", image=icons['big_pdf'])
        self.empty_text = ctk.CTkLabel(
            self, text=TEXTS['empty_msg'],
            text_color=COLOR_TEXT_SECONDARY
        )

        self.empty_icon.place(relx=0.5, rely=0.4, anchor="center")
        self.empty_text.place(relx=0.5, rely=0.6, anchor="center")

        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", on_drop_callback)

    def update_view(self, files, selected_index):
        for child in self.list_frame.winfo_children():
            child.destroy()

        if not files:
            self.empty_icon.place(relx=0.5, rely=0.4, anchor="center")
            self.empty_text.place(relx=0.5, rely=0.6, anchor="center")
        else:
            self.empty_icon.place_forget()
            self.empty_text.place_forget()
            
            for i, path in enumerate(files):
                item = FileItem(
                    master=self.list_frame,
                    path=path,
                    index=i,
                    is_selected=(selected_index == i),
                    icon_pdf=self.icons['pdf'],
                    on_select=self.on_select,
                    on_delete=self.on_delete
                )
                item.pack(fill="x", pady=2, padx=5)