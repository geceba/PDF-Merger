import customtkinter as ctk
from src.core.pdf_engine import get_page_thumbnails
from src.utils.constants import COLOR_DEFAULT, COLOR_DEFAULT_HOVER, COLOR_SELECT_TO_DELETE, COLOR_SELECT_TO_DELETE_BORDER

class PagePreviewPanel(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=400, label_text="Vista Previa", **kwargs)
        self.pages = []
        self.selected_pages = set()
    
    def load_pdf(self, pdf_path):
        for widget in self.winfo_children():
            widget.destroy()
        self.selected_pages.clear()

        thumbnails = get_page_thumbnails(pdf_path)

        for i, img in enumerate(thumbnails):
            img_ctk = ctk.CTkImage(img, size=(120, 160))

            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=i//3, column=i%3, padx=10, pady=10)

            lbl = ctk.CTkButton(
                frame, 
                image=img_ctk, 
                text=f"Pág {i+1}", 
                compound="top",
                fg_color=COLOR_DEFAULT,
                hover_color=COLOR_DEFAULT_HOVER,
                command=lambda idx=i: self.toggle_page(idx)
            )
            lbl.pack()
            self.pages.append(lbl)

    def toggle_page(self, index):
        if index in self.selected_pages:
            self.selected_pages.remove(index)
            self.pages[index].configure(fg_color=COLOR_DEFAULT, border_width=0)
        else:
            self.selected_pages.add(index)
            self.pages[index].configure(fg_color=COLOR_SELECT_TO_DELETE, border_width=2, border_color=COLOR_SELECT_TO_DELETE_BORDER)


