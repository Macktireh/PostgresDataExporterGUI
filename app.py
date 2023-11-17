import csv
import os
from tkinter import filedialog
import customtkinter as ctk

from interface import IServiceDataProcessor


ctk.set_appearance_mode("dark")


class App(ctk.CTk):
    pathDirectory: str
    toggle: bool = False

    def __init__(self, serviceDataProcessor: IServiceDataProcessor) -> None:
        super().__init__()
        self.title("Postgres table to CSV App")
        self.geometry("700x700")
        self.serviceDataProcessor = serviceDataProcessor

        self.heading = ctk.CTkLabel(
            self,
            text="Postgres table to CSV App",
            font=("arial", 30, "bold"),
            text_color=("#000", "#FFF"),
        )
        self.heading.pack(pady=20)

        self.frameQuery = ctk.CTkFrame(
            self,
            width=540,
            height=280,
        )
        self.frameQuery.pack(pady=10)

        self.labelQuery = ctk.CTkLabel(
            self.frameQuery,
            text="Enter your SQL query:",
            font=("arial", 12, "bold"),
            text_color=("#000", "#FFF"),
        )
        self.labelQuery.place(x=10, y=10)
        self.query = ctk.CTkTextbox(
            self.frameQuery,
            width=520,
            height=230,
            corner_radius=10,
            font=("arial", 16, "bold"),
            text_color=("#000", "#FFF"),
        )
        self.query.place(x=10, y=40)
        self.query.insert("0.0", "SELECT * FROM imgtest.data_passeport_client")

        self.frameEntry = ctk.CTkFrame(
            self,
            bg_color="transparent",
            # width=540,
            # height=280,
        )
        self.frameEntry.pack(pady=10)

        self.entryIndexImage = ctk.CTkEntry(
            self.frameEntry,
            placeholder_text="Index of image column",
            font=("arial", 12, "bold"),
            text_color=("#000", "#FFF"),
            width=350,
        )
        self.entryIndexImage.pack(pady=5)
        self.entryIndexImage.insert(0, "-1")

        self.entryIndexName = ctk.CTkEntry(
            self.frameEntry,
            placeholder_text="Column index for image name",
            font=("arial", 12, "bold"),
            text_color=("#000", "#FFF"),
            width=350,
        )
        # witdth 100%
        self.entryIndexName.pack(pady=5)
        self.entryIndexName.insert(0, "0")

        self.framePath = ctk.CTkFrame(
            self,
            width=540,
            fg_color="transparent",
            # height=1,
        )
        self.framePath.pack(pady=5)

        self.labelPathDir = ctk.CTkLabel(
            self.framePath,
            text="",
            font=("arial", 12, "bold"),
            text_color=("#000", "#FFF"),
        )
        self.labelPathDir.pack(pady=1)

        self.buttonPathDirectory = ctk.CTkButton(
            self.framePath,
            text="Choose directory",
            font=("arial", 12, "bold"),
            text_color=("#000", "#FFF"),
            command=self.askExportDirectory,
            width=350,
            height=40,
        )
        self.buttonPathDirectory.pack(pady=1)

        self.buttonExport = ctk.CTkButton(
            self,
            text="Export",
            font=("arial", 14, "bold"),
            text_color=("#000", "#FFF"),
            command=self.export,
            width=350,
            height=40,
        )
        self.buttonExport.pack(pady=10)

    def start(self) -> None:
        self.mainloop()

    def displayProgress(self) -> None:
        if not self.toggle:
            self.frameProgress.pack()
            self.toggle = True
        else:
            self.frameProgress.pack_forget()
            self.toggle = False

    def askExportDirectory(self) -> str:
        self.pathDirectory = filedialog.askdirectory()
        self.labelPathDir.configure(text=self.pathDirectory)
        self.labelPathDir.update()
        return self.pathDirectory

    def export(self) -> None:
        self.frameProgress = ctk.CTkFrame(
            self,
            width=540,
            bg_color="transparent",
            fg_color="transparent",
        )
        self.frameProgress.pack(pady=10)

        self.labelProgress = ctk.CTkLabel(
            self.frameProgress,
            text="",
            font=("arial", 12, "bold"),
            text_color=("#000", "#FFF"),
        )
        self.labelProgress.pack(pady=2)

        self.progress = ctk.CTkProgressBar(self.frameProgress, orientation="horizontal")
        self.progress.pack()
        self.progress.set(0)

        query = self.query.get("1.0", "end-1c")
        record, colNames = self.serviceDataProcessor.fetchData(query)

        pathImages = self.pathDirectory + "/images"
        if not os.path.exists(pathImages):
            os.makedirs(pathImages)

        with open(f"{self.pathDirectory}/output.csv", "w", newline="") as f:
            writer = csv.writer(f)
            colNames[-1] = "image"
            writer.writerow(colNames)
            for i, row in enumerate(record):
                self.serviceDataProcessor.exportToCSV2(
                    row,
                    pathImages,
                    writer,
                    int(self.entryIndexImage.get()),
                    int(self.entryIndexName.get()),
                )
                valueProgress = int((i + 1) / len(record) * 100)
                print(valueProgress)
                self.progress.set(valueProgress)
                self.labelProgress.configure(text=f"{valueProgress}%")
                self.labelProgress.update()
