import customtkinter as ctk


class Input(ctk.CTkFrame):
    def __init__(
        self,
        master: ctk.CTkBaseClass,
        label: str = "Input",
        width: int = 300,
        height: int = 50,
        defaultValue: str = "",
        isPassword: bool = False,
        state: str = "normal",
    ) -> None:
        self.master = master
        self.label = label
        self.width = width
        self.height = height
        self.defaultValue = defaultValue
        self.isPassword = isPassword
        self.state = state

        super().__init__(self.master, width=self.width, height=self.height)

        self.label = ctk.CTkLabel(self, text=self.label, width=self.width // 3)
        self.label.pack(side="left", padx=5, pady=5)

        self.entry = ctk.CTkEntry(self, width=(self.width * 3) // 3, state=self.state)
        self.entry.pack(side="right", padx=5, pady=5)
        self.entry.insert(0, self.defaultValue)

        if self.isPassword:
            self.entry.configure(show="*")

    def getValueInput(self) -> str:
        return self.entry.get()

    def setValueInput(self, value: str) -> None:
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        self.entry.update()

    def clear(self) -> None:
        self.entry.delete(0, "end")
        self.entry.update()
