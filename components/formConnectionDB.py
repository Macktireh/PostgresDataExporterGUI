from tkinter import messagebox
import customtkinter as ctk

from components.input import Input
from service.api import ParamsConnection


class FormConnectionDB(ctk.CTkFrame):
    def __init__(
        self, master: ctk.CTkBaseClass, width: int = 600, height: int = 50
    ) -> None:
        self.master = master
        self.width = width
        self.height = height

        super().__init__(self.master, width=self.width, height=self.height)

        self.username = Input(
            self, label="Username", width=220
        )
        self.password = Input(self, label="Password", width=220, isPassword=True)
        self.host = Input(self, label="Host", width=220, defaultValue="localhost")
        self.port = Input(self, label="Port", width=220, defaultValue="5432")
        self.database = Input(self, label="Database", width=220, height=50)

        self.username.grid(row=0, column=0, padx=5, pady=5)
        self.password.grid(row=0, column=1, padx=5, pady=5)
        self.host.grid(row=1, column=0, padx=5, pady=5)
        self.port.grid(row=1, column=1, padx=5, pady=5)
        self.database.grid(row=2, column=0, padx=5, pady=5)

    def getFormData(self) -> ParamsConnection:
        return {
            "database": self.database.getValueInput(),
            "user": self.username.getValueInput(),
            "password": self.password.getValueInput(),
            "host": self.host.getValueInput(),
            "port": self.port.getValueInput(),
        }

    def validateFormData(self) -> bool:
        if not self.username.getValueInput():
            messagebox.showerror("Erreur", "Le champ USERNAME est obligatoire")
            return False
        if not self.password.getValueInput():
            messagebox.showerror("Erreur", "Le champ PASSWORD est obligatoire")
            return False
        if not self.host.getValueInput():
            messagebox.showerror("Erreur", "Le champ HOST est obligatoire")
            return False
        if not self.port.getValueInput():
            messagebox.showerror("Erreur", "Le champ PORT est obligatoire")
            return False
        if not self.database.getValueInput():
            messagebox.showerror("Erreur", "Le champ DATABASE est obligatoire")
            return False
        return True
