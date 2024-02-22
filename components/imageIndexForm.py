import customtkinter as ctk
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager

from components.input import Input


class ImageIndexForm(ctk.CTkFrame):
    def __init__(
        self, master: ctk.CTkBaseClass, width: int = 600, height: int = 50
    ) -> None:
        self.master = master
        self.width = width
        self.height = height

        super().__init__(self.master, width=self.width, height=self.height)

        self.hasImage = ctk.CTkCheckBox(
            self,
            text="J'ai une colonne d'image",
            font=("arial", 12, "bold"),
            text_color=("#000", "#FFF"),
            onvalue=1,
            offvalue=0,
            command=self.onCheck,
        )
        self.imageColumnIndex = Input(self, label="Index colonne images", width=120, state="disabled")

        self.hasImage.grid(row=0, column=0, padx=5, pady=5)
        self.imageColumnIndex.grid(row=0, column=1, padx=5, pady=5)

        self.handleDisable()

    def getValueInput(self) -> str:
        return self.imageColumnIndex.getValueInput()

    def getValueCheckbox(self) -> int | str:
        return self.hasImage.get()

    def onCheck(self) -> None:
        if self.getValueCheckbox() == 1:
            self.handleEnable()
        else:
            self.handleDisable()

    def handleDisable(self) -> None:
        self.imageColumnIndex.entry.configure(state="disabled", fg_color="#4f4f4f")
        self.imageColumnIndex.label.configure(text_color="#4f4f4f")

    def handleEnable(self) -> None:
        self.imageColumnIndex.entry.configure(
            state="normal", fg_color=ThemeManager.theme["CTkEntry"]["fg_color"]
        )
        self.imageColumnIndex.label.configure(
            text_color=ThemeManager.theme["CTkLabel"]["text_color"]
        )
