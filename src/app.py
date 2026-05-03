import customtkinter as ctk
import ctypes
from pypdf import PdfReader
from PIL import Image
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD

from src.components.action_buttons import ActionButtons
from src.components.file_list import FileListContainer
from src.components.preview_panel import PagePreviewPanel
from src.core.pdf_engine import merge_pdfs, open_file
from src.core.doc_engine import DocEngine
from src.utils.helpers import resource_path
from src.utils.i18n import TEXTS

myappid = 'just.pdfmerger' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF Merger")
        self.geometry("1100x600")
        self.iconbitmap(resource_path("icons/favicon.ico"))

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)  

        self.pdf_configs = {} 

        self.icon_merge = ctk.CTkImage(Image.open(resource_path("icons/link.png")), size=(20, 20))
        self.icons = {
            "add": ctk.CTkImage(Image.open(resource_path("icons/plus.png")), size=(20, 20)),
            "trash": ctk.CTkImage(Image.open(resource_path("icons/trash-2.png")), size=(20, 20)),
            "up": ctk.CTkImage(Image.open(resource_path("icons/square-chevron-up.png")), size=(20, 20)),
            "down": ctk.CTkImage(Image.open(resource_path("icons/square-chevron-down.png")), size=(20, 20)),
            "big_pdf": ctk.CTkImage(Image.open(resource_path("icons/file-plus-corner.png")), size=(100, 100)),
            "pdf": ctk.CTkImage(Image.open(resource_path("icons/pdf.png")), size=(24, 24)),
            "right_arrow": ctk.CTkImage(Image.open(resource_path("icons/chevron-right.png")), size=(15, 15)),
            "left_arrow": ctk.CTkImage(Image.open(resource_path("icons/chevron-left.png")), size=(15, 15)),
            "doc": ctk.CTkImage(Image.open(resource_path("icons/doc.png")), size=(24, 24))
        }

        self.left_panel = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.pdf_list_view = FileListContainer(
            self.left_panel, 
            icons=self.icons,
            on_drop_callback=self.drop,
            on_select=self.select,
            on_delete=self.delete_item,
            on_convert=self.convert_to_word
        )
        self.pdf_list_view.pack(fill="both", expand=True)

        self.files = []
        self.selected_index = None

        commands = {
            "add": self.add,
            "clear": self.clear,
            "up": self.up,
            "down": self.down
        }

        self.buttons_view = ActionButtons(self.left_panel, self.icons, commands)
        self.buttons_view.pack(pady=10)

        self.preview_view = PagePreviewPanel(
            self.frame, 
            on_config_change=self.update_pdf_configs,
            icons=self.icons,
        )

        self.progress = ctk.CTkProgressBar(self.frame)
        self.progress.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        self.progress.set(0)

        self.merge_btn = ctk.CTkButton(
            self.frame, 
            text=TEXTS['btn_merge'], 
            image=self.icon_merge, 
            compound="right", 
            fg_color="#10897B", 
            hover_color="#075E54", 
            height=40, 
            width=200,
            command=self.join
        )
        self.merge_btn.grid(row=2, column=0, columnspan=2, pady=10)
    
    def update_pdf_configs(self, path, new_order, new_excluded):
        self.pdf_configs[path] = {
            "order": list(new_order),
            "excluded": set(new_excluded)
        }

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

        if index is not None and index < len(self.files):
            path = self.files[index]

            self.frame.columnconfigure(0, weight=0)
            self.frame.columnconfigure(1, weight=1)
            
            self.preview_view.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
            saved_conf = self.pdf_configs.get(path)
            self.preview_view.load_pdf(path, saved_config=saved_conf)
        else: 
            self.close_preview_dinamically()

    def add(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if files:
            for file in files:
                if file not in self.files:
                    self.files.append(file)

                    try:
                        reader = PdfReader(file)
                        num_pages = len(reader.pages)
                        self.pdf_configs[file] = {
                            "order": list(range(num_pages)),
                            "excluded": set()
                        }
                    except Exception as e:
                        print(f"Error {file}: {e}")

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
        self.selected_index = None
        self.close_preview_dinamically()
        self.update_list()

    def delete_item(self, index):
        self.files.pop(index)
        
        if self.selected_index == index:
            self.selected_index = None
            self.close_preview_dinamically()
        elif self.selected_index is not None and self.selected_index > index:
            self.selected_index -= 1
            
        self.update_list()
    
    def convert_to_word(self, path):
        success, result = DocEngine.convert_pdf_to_word(path)
        if success:
            open_file(result)
            messagebox.showinfo(TEXTS['success_title'], TEXTS['msg_conversion_success'])
        else:
            messagebox.showerror(TEXTS['error_title'], result)

    def drop(self, event):
        files = self.tk.splitlist(event.data)
        for f in files:
            if f.lower().endswith(".pdf"):
                self.files.append(f)
        self.update_list()

    def join(self):
        if not self.files:
            messagebox.showwarning(TEXTS['warning_title'], TEXTS['msg_no_pdfs'])
            return

        output = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not output:
            return

        try:
            merge_pdfs(self.files, self.pdf_configs, output, progress_callback=self.progress.set)
            open_file(output)
            messagebox.showinfo(TEXTS['success_title'], TEXTS['msg_success'])

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def close_preview_dinamically(self):
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)
        self.preview_view.grid_forget()
        
