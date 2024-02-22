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

        self.username = Input(self, label="Username", width=220)
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
            "user": self.username.getValueInput(),
            "password": self.password.getValueInput(),
            "host": self.host.getValueInput(),
            "port": self.port.getValueInput(),
            "database": self.database.getValueInput(),
        }

    def validateFormData(self) -> bool:
        form_data = self.getFormData()
        for field_key, value in form_data.items():
            if not value:
                field_name_capitalized = field_key.capitalize() if field_key != "user" else "Username"
                messagebox.showerror("Erreur", f"Le champ {field_name_capitalized} est obligatoire")
                return False
        return True
