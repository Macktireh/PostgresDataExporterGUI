import csv
import os
from tkinter import filedialog, messagebox

import customtkinter as ctk
from components.formConnectionDB import FormConnectionDB
from components.imageIndexForm import ImageIndexForm
from components.progressBar import ProgressBar
from components.textarea import TextArea
from service.api import PostgreSQLConnection, ServiceDataProcessor
from service.exception import DBConnectionException, DBQueryException


ctk.set_appearance_mode("dark")


class App(ctk.CTk):
    pathDirectory: str = None
    toggle: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.title("PostgresDataExporterGUI")
        self.geometry("700x700")
        self.resizable(False, False)

        self.formConnectionDB = FormConnectionDB(self)
        self.formConnectionDB.pack(pady=30)

        self.query = TextArea(self, label="Requête SQL :", width=644, height=200)
        self.query.pack()

        self.imageIndexForm = ImageIndexForm(self)
        self.imageIndexForm.pack(pady=30)

        self.labelPathDir = ctk.CTkLabel(self, text="", font=("arial", 12, "bold"), text_color=("#000", "#FFF"))
        self.labelPathDir.pack(pady=5)

        self.frameBtn = ctk.CTkFrame(self, fg_color="transparent")
        self.frameBtn.pack(pady=10)

        self.buttonPathDirectory = ctk.CTkButton(
            self.frameBtn,
            text="Choisir un dossier",
            font=("arial", 12, "bold"),
            text_color=("#000", "#FFF"),
            fg_color="#474545",
            hover_color="#333131",
            command=self.askExportDirectory,
            width=300,
            height=40,
        )
        self.buttonPathDirectory.grid(row=0, column=0, padx=10)

        self.buttonExport = ctk.CTkButton(
            self.frameBtn,
            text="Exporter",
            font=("arial", 14, "bold"),
            text_color=("#000", "#FFF"),
            command=self.export,
            width=300,
            height=40,
        )
        self.buttonExport.grid(row=0, column=1, padx=10)

    def start(self) -> None:
        self.mainloop()

    def askExportDirectory(self) -> str:
        self.pathDirectory = filedialog.askdirectory()
        self.labelPathDir.configure(text=self.pathDirectory)
        self.labelPathDir.update()
        return self.pathDirectory

    def export(self) -> None:
        if not self.formConnectionDB.validateFormData():
            return

        if not self.pathDirectory:
            messagebox.showerror("Error", "Veuillez choisir un dossier")
            return

        if not self.query.getText():
            messagebox.showerror("Error", "Veuillez saisir une requête SQL")
            return

        if self.imageIndexForm.getValueCheckbox() == 1:
            if not self.imageIndexForm.getValueInput():
                messagebox.showerror("Error", "Veuillez saisir l'index de la colonne d'images")
                return
            # check if self.imageIndexForm.getValueInput() is a number
            try:
                int(self.imageIndexForm.getValueInput())
            except ValueError:
                messagebox.showerror("Error", "Veuillez saisir un nombre valide pour l'index de la colonne d'images")
                return

        self.buttonExport.configure(state="disabled")
        self.progress = ProgressBar(self)
        self.progress.pack(pady=10)

        params = self.formConnectionDB.getFormData()
        postgreSQLConnection = PostgreSQLConnection(params=params)
        serviceDataProcessor = ServiceDataProcessor(connection=postgreSQLConnection)

        try:
            record, colNames = serviceDataProcessor.fetchData(self.query.getText())
        except DBConnectionException as e:
            messagebox.showerror("Error", e.message)
            self.progress.destroy()
            self.buttonExport.configure(state="normal")
            return
        except DBQueryException as e:
            messagebox.showerror("Error", e.message)
            self.progress.destroy()
            self.buttonExport.configure(state="normal")
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            self.progress.destroy()
            self.buttonExport.configure(state="normal")
            return

        if self.imageIndexForm.getValueCheckbox() == 1:
            pathImages = self.pathDirectory + "/images"
            if not os.path.exists(pathImages):
                os.makedirs(pathImages)
        else:
            pathImages = None

        with open(
            f"{self.pathDirectory}/data.csv", "w", newline="", encoding="utf-8"
        ) as f:
            try:
                writer = csv.writer(f)
                if self.imageIndexForm.getValueCheckbox() == 1:
                    colNames[int(self.imageIndexForm.getValueInput())] = "image"
                writer.writerow(colNames)
                for i, row in enumerate(record):
                    serviceDataProcessor.exportToCSV2(
                        row,
                        writer,
                        self.imageIndexForm.getValueCheckbox() == 1,
                        pathImages,
                        int(self.imageIndexForm.getValueInput()),
                    )
                    valueProgress = int((i + 1) / len(record) * 100)
                    print(f"{valueProgress}%", "row", i + 1, "of", len(record))
                    self.progress.setProgress(valueProgress / 100)
            except Exception as e:
                messagebox.showerror("Error", e)
                self.progress.destroy()
                self.buttonExport.configure(state="normal")
                return

        messagebox.showinfo(
            "Success",
            f"Le fichier {self.pathDirectory}/data.csv a été exporté avec success",
        )

        self.progress.destroy()
        self.buttonExport.configure(state="normal")


if __name__ == "__main__":
    App().start()
