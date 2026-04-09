import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import customtkinter as ctk
import os
import ctypes

from src.components.action_buttons import ActionButtons
from src.core.pdf_engine import merge_pdfs, open_file
from src.utils.helpers import resource_path

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

        self.container_list = ctk.CTkFrame(self.frame, fg_color="#1e1e1e", corner_radius=12)
        self.container_list.pack(fill="both", expand=True, pady=10)

        self.list_frame = ctk.CTkScrollableFrame(
            self.container_list, 
            fg_color="transparent",
            scrollbar_button_color="#333333"
        )
        self.list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.icon_big_pdf = ctk.CTkImage(Image.open(resource_path("icons/file-plus-corner.png")), size=(100, 100))
        self.empty_icon_label = ctk.CTkLabel(self.container_list, text="", image=self.icon_big_pdf)
        self.empty_icon_label.place(relx=0.5, rely=0.4, anchor="center")

        self.empty_text_label = ctk.CTkLabel(
            self.container_list, 
            text="Arrastra PDFs aquí o haz clic en 'Agregar'",
            text_color="#666666",
        )
        self.empty_text_label.place(relx=0.5, rely=0.6, anchor="center")

        self.selected_index = None

        # cargar icono
        self.icono_pdf = ctk.CTkImage(Image.open(resource_path("icons/pdf.png")), size=(24, 24))
        self.icon_merge = ctk.CTkImage(Image.open(resource_path("icons/link.png")), size=(20, 20))

        self.icons = {
            "add": ctk.CTkImage(Image.open(resource_path("icons/plus.png")), size=(20, 20)),
            "trash": ctk.CTkImage(Image.open(resource_path("icons/trash-2.png")), size=(20, 20)),
            "up": ctk.CTkImage(Image.open(resource_path("icons/square-chevron-up.png")), size=(20, 20)),
            "down": ctk.CTkImage(Image.open(resource_path("icons/square-chevron-down.png")), size=(20, 20)),
        }

        self.files = []

        # Drag & Drop
        self.container_list.drop_target_register(DND_FILES)
        self.container_list.dnd_bind("<<Drop>>", self.drop)

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
            text="Unir PDFs", 
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
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for i, path in enumerate(self.files):
            name = os.path.basename(path)

            item = ctk.CTkFrame(self.list_frame)
            item.pack(fill="x", pady=2, padx=5)

            if self.selected_index == i:
                item.configure(fg_color="#3a7ebf")


            icon = ctk.CTkLabel(item, image=self.icono_pdf, text="", cursor="hand2")
            icon.pack(side="left", padx=10)

            label = ctk.CTkLabel(item, text=name, cursor="hand2")
            label.pack(side="left", padx=5)

            btn_eliminar = ctk.CTkButton(
                item, 
                text="✕", 
                width=28, 
                height=28,
                fg_color="transparent",
                hover_color="#E74C3C",
                text_color="#FFFFFF",
                corner_radius=6,
                command=lambda idx=i: self.delete_item(idx)
            )
            btn_eliminar.pack(side="right", padx=10)

            item.bind("<Button-1>", lambda e, idx=i: self.select(idx))
            label.bind("<Button-1>", lambda e, idx=i: self.select(idx))
            icon.bind("<Button-1>", lambda e, idx=i: self.select(idx))

        self.update_empty_state()
    
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
        for a in files:
            if a.endswith(".pdf"):
                self.files.append(a)
        self.update_list()

    def select(self, index):
        self.selected_index = index
        self.update_list()

    def join(self):
        if not self.files:
            messagebox.showwarning("Aviso", "No hay PDFs")
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
