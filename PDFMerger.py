import customtkinter as ctk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import customtkinter as ctk
import os
import sys
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF Merger 🔥")
        self.geometry("700x500")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.label = ctk.CTkLabel(self.frame, text="Arrastra PDFs aquí 👇")
        self.label.pack(pady=10)

        self.lista_frame = ctk.CTkScrollableFrame(self.frame)
        self.lista_frame.pack(fill="both", expand=True, pady=10)

        self.selected_index = None

        # cargar icono
        self.icono_pdf = ctk.CTkImage(Image.open("icons/pdf.png"), size=(24, 24))

        self.archivos = []

        # Drag & Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.drop)

        botones = ctk.CTkFrame(self.frame)
        botones.pack(pady=10)

        ctk.CTkButton(botones, text="Agregar", command=self.agregar).grid(row=0, column=0, padx=5)
        ctk.CTkButton(botones, text="Limpiar", command=self.limpiar).grid(row=0, column=1, padx=5)
        ctk.CTkButton(botones, text="Subir ↑", command=self.subir).grid(row=0, column=2, padx=5)
        ctk.CTkButton(botones, text="Bajar ↓", command=self.bajar).grid(row=0, column=3, padx=5)

        self.progress = ctk.CTkProgressBar(self.frame)
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)

        ctk.CTkButton(self.frame, text="Unir PDFs", command=self.unir).pack(pady=10)

    def actualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        for i, ruta in enumerate(self.archivos):
            nombre = os.path.basename(ruta)

            item = ctk.CTkFrame(self.lista_frame)
            item.pack(fill="x", pady=2, padx=5)

            if self.selected_index == i:
                item.configure(fg_color="#3a7ebf")

            item.bind("<Button-1>", lambda e, idx=i: self.seleccionar(idx))

            icon = ctk.CTkLabel(item, image=self.icono_pdf, text="")
            icon.pack(side="left", padx=5)

            label = ctk.CTkLabel(item, text=nombre)
            label.pack(side="left", padx=5)

            label.bind("<Button-1>", lambda e, idx=i: self.seleccionar(idx))
            icon.bind("<Button-1>", lambda e, idx=i: self.seleccionar(idx))
    
    def seleccionar(self, index):
        self.selected_index = index
        self.actualizar_lista()

    def agregar(self):
        archivos = filedialog.askopenfilenames(filetypes=[("PDF", "*.pdf")])
        self.archivos.extend(archivos)
        self.actualizar_lista()
    
    def subir(self):
        i = self.selected_index
        if i is None or i == 0:
            return

        self.archivos[i], self.archivos[i - 1] = self.archivos[i - 1], self.archivos[i]
        self.selected_index = i - 1
        self.actualizar_lista()
    
    def bajar(self):
        i = self.selected_index
        if i is None or i >= len(self.archivos) - 1:
            return

        self.archivos[i], self.archivos[i + 1] = self.archivos[i + 1], self.archivos[i]
        self.selected_index = i + 1
        self.actualizar_lista()

    def limpiar(self):
        self.archivos = []
        self.actualizar_lista()

    def drop(self, event):
        archivos = self.tk.splitlist(event.data)
        for a in archivos:
            if a.endswith(".pdf"):
                self.archivos.append(a)
        self.actualizar_lista()

    def seleccionar(self, index):
        self.selected_index = index
        self.actualizar_lista()

    def unir(self):
        if not self.archivos:
            messagebox.showwarning("Aviso", "No hay PDFs")
            return

        salida = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not salida:
            return

        merger = PdfMerger()

        try:
            total = len(self.archivos)

            for i, pdf in enumerate(self.archivos):
                merger.append(pdf)
                self.progress.set((i + 1) / total)
                self.update()

            merger.write(salida)
            merger.close()

            self.abrir(salida)

            messagebox.showinfo("Éxito", "🔥 PDF listo")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir(self, ruta):
        try:
            if sys.platform == "win32":
                os.startfile(ruta)
            elif sys.platform == "darwin":
                subprocess.call(["open", ruta])
            else:
                subprocess.call(["xdg-open", ruta])
        except:
            pass


if __name__ == "__main__":
    app = App()
    app.mainloop()