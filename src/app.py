import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD
from PIL import Image
import customtkinter as ctk
import ctypes

from src.components.action_buttons import ActionButtons
from src.components.file_list import FileListContainer
from src.core.pdf_engine import merge_pdfs, open_file
from src.utils.helpers import resource_path
from src.utils.i18n import TEXTS

myappid = 'just.pdfmerger' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF Merger")
        self.geometry("700x500")
        self.iconbitmap(resource_path("icons/favicon.ico"))

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.icon_merge = ctk.CTkImage(Image.open(resource_path("icons/link.png")), size=(20, 20))

        self.icons = {
            "add": ctk.CTkImage(Image.open(resource_path("icons/plus.png")), size=(20, 20)),
            "trash": ctk.CTkImage(Image.open(resource_path("icons/trash-2.png")), size=(20, 20)),
            "up": ctk.CTkImage(Image.open(resource_path("icons/square-chevron-up.png")), size=(20, 20)),
            "down": ctk.CTkImage(Image.open(resource_path("icons/square-chevron-down.png")), size=(20, 20)),
            "big_pdf": ctk.CTkImage(Image.open(resource_path("icons/file-plus-corner.png")), size=(100, 100)),
            "pdf": ctk.CTkImage(Image.open(resource_path("icons/pdf.png")), size=(24, 24))
        }

        self.pdf_list_view = FileListContainer(
            self.frame, 
            icons=self.icons,
            on_drop_callback=self.drop,
            on_select=self.select,
            on_delete=self.delete_item
        )

        self.pdf_list_view.pack(fill="both", expand=True, pady=10)

        self.files = []
        self.selected_index = None

        commands = {
            "add": self.add,
            "clear": self.clear,
            "up": self.up,
            "down": self.down
        }

        self.buttons_view = ActionButtons(self.frame, self.icons, commands)
        self.buttons_view.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self.frame)
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)

        ctk.CTkButton(
            self.frame, 
            text=TEXTS['btn_merge'], 
            image=self.icon_merge, 
            compound="right", 
            fg_color="#10897B", 
            hover_color="#075E54", 
            height=40, 
            width=200,
            command=self.join).pack(pady=10)
    
    def update_empty_state(self): 
        if hasattr(self, 'files') and len(self.files) > 0:
            self.empty_icon_label.place_forget()
            self.empty_text_label.place_forget()
        else:
            self.empty_icon_label.place(relx=0.5, rely=0.4, anchor="center")
            self.empty_text_label.place(relx=0.5, rely=0.6, anchor="center")

    def update_list(self):
        self.pdf_list_view.update_view(self.files, self.selected_index)
    
    def select(self, index):
        self.selected_index = index
        self.update_list()

    def add(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF", "*.pdf")])
        self.files.extend(files)
        self.update_list()
    
    def up(self):
        i = self.selected_index
        if i is None or i == 0:
            return

        self.files[i], self.files[i - 1] = self.files[i - 1], self.files[i]
        self.selected_index = i - 1
        self.update_list()
    
    def down(self):
        i = self.selected_index
        if i is None or i >= len(self.files) - 1:
            return

        self.files[i], self.files[i + 1] = self.files[i + 1], self.files[i]
        self.selected_index = i + 1
        self.update_list()

    def clear(self):
        self.files = []
        self.update_list()

    def delete_item(self, index):
        self.files.pop(index)
        
        if self.selected_index == index:
            self.selected_index = None
        elif self.selected_index is not None and self.selected_index > index:
            self.selected_index -= 1
            
        self.update_list()

    def drop(self, event):
        files = self.tk.splitlist(event.data)
        for f in files:
            if f.lower().endswith(".pdf"):
                self.files.append(f)
        self.update_list()

    def select(self, index):
        self.selected_index = index
        self.update_list()

    def join(self):
        if not self.files:
            messagebox.showwarning("Aviso", TEXTS['msg_no_pdfs'])
            return

        output = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not output:
            return

        try:
            merge_pdfs(self.files, output, progress_callback=self.progress.set)
            open_file(output)
            messagebox.showinfo("Éxito", "🔥 PDF listo")

        except Exception as e:
            messagebox.showerror("Error", str(e))
