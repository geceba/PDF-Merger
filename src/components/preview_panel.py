import customtkinter as ctk
from pypdf import PdfReader
from src.core.pdf_engine import get_page_thumbnails
from src.utils.i18n import TEXTS
from src.utils.constants import COLOR_DEFAULT, COLOR_DEFAULT_HOVER, COLOR_SELECT_TO_DELETE, COLOR_SELECT_TO_DELETE_HOVER

class PagePreviewPanel(ctk.CTkScrollableFrame):
    def __init__(self, master, on_config_change=None, icons=None, **kwargs):
        super().__init__(master, width=420, label_text=TEXTS['preview_title'], **kwargs)
        self.on_config_change = on_config_change
        self.icons = icons
        self.current_order = []
        self.selected_pages = set()
    
    def toggle_exclude(self, page_index, pdf_path):
        if page_index in self.selected_pages:
            self.selected_pages.remove(page_index)
        else:
            self.selected_pages.add(page_index)
        
        if self.on_config_change:
            self.on_config_change(pdf_path, self.current_order, self.selected_pages)
        
        self.render_pages(pdf_path)
    
    def move(self, display_idx, direction, pdf_path):
        new_idx = display_idx + direction
        if 0 <= new_idx < len(self.current_order):
            self.current_order[display_idx], self.current_order[new_idx] = \
                self.current_order[new_idx], self.current_order[display_idx]
            
            if self.on_config_change:
                self.on_config_change(pdf_path, self.current_order, self.selected_pages)
            
            self.render_pages(pdf_path)
    
    def load_pdf(self, pdf_path, saved_config = None):
        for widget in self.winfo_children():
            widget.destroy()
        
        if not saved_config:
            num_pages = len(PdfReader(pdf_path).pages)
            self.current_order = list(range(num_pages))
            self.selected_pages = set()
        else:
            self.current_order = list(saved_config["order"])
            self.selected_pages = set(saved_config["excluded"])
        
        self.render_pages(pdf_path)
    
    def render_pages(self, pdf_path):
        for widget in self.winfo_children():
            widget.destroy()
            
        thumbnails = get_page_thumbnails(pdf_path)
        total_pages = len(thumbnails)

        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        for display_idx, page_idx in enumerate(self.current_order):
            is_excluded = page_idx in self.selected_pages

            current_fg = COLOR_SELECT_TO_DELETE if is_excluded else COLOR_DEFAULT
            current_hover = COLOR_SELECT_TO_DELETE_HOVER if is_excluded else COLOR_DEFAULT_HOVER

            container = ctk.CTkFrame(self, fg_color=current_fg)
            container.grid(row=display_idx//2, column=display_idx%2, padx=10, pady=10, sticky="ew")

            img_ctk = ctk.CTkImage(thumbnails[page_idx], size=(120, 160))
            btn = ctk.CTkButton(
                container, image=img_ctk, text=f"Pag {page_idx + 1}",
                fg_color=current_fg,
                hover_color=current_hover,
                command=lambda p=page_idx: self.toggle_exclude(p, pdf_path)
            )

            btn.pack()

            if not is_excluded and total_pages > 1:
                ctrl_frame = ctk.CTkFrame(container, fg_color="transparent")
                ctrl_frame.pack(fill="x", pady=2)

                if display_idx > 0:
                    ctk.CTkButton(
                            ctrl_frame, text="", image=self.icons["left_arrow"], width=30, 
                            command=lambda i=display_idx: self.move(i, -1, pdf_path)
                        ).pack(side="left", expand=True, padx=2)
                else:
                    ctk.CTkLabel(ctrl_frame, text="", width=30).pack(side="left", expand=True)

                if display_idx < total_pages - 1:
                    ctk.CTkButton(
                        ctrl_frame, text="", image=self.icons["right_arrow"], width=30, 
                        command=lambda i=display_idx: self.move(i, 1, pdf_path)
                    ).pack(side="right", expand=True, padx=2)
                else:
                    ctk.CTkLabel(ctrl_frame, text="", width=30).pack(side="right", expand=True)
            elif is_excluded:
                ctk.CTkLabel(container, text=TEXTS['exclude_label'], text_color="#ffffff", 
                            font=("Arial", 10, "bold")).pack(pady=2)    

            
