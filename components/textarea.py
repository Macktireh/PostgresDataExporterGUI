import customtkinter as ctk


class TextArea(ctk.CTkFrame):
    def __init__(
        self,
        master: ctk.CTkBaseClass,
        label: str = "TextArea",
        width: int = 300,
        height: int = 100,
        defaultValue: str = "",
    ) -> None:
        self.master = master
        self.label = label
        self.width = width
        self.height = height
        self.defaultValue = defaultValue

        super().__init__(self.master, width=self.width, height=self.height)

        self.label = ctk.CTkLabel(self, text=self.label)
        self.label.place(x=5, y=5)

        self.entry = ctk.CTkTextbox(
            self,
            font=("Arial", 14),
            wrap="word",
            corner_radius=10,
            text_color=("#000", "#FFF"),
            width=int(self.width * 0.985),
            height=int(self.height - 40),
        )
        self.entry.place(x=5, y=35)
        self.entry.insert("1.0", self.defaultValue)

    def getText(self) -> str:
        return self.entry.get("1.0", "end-1c")

    def setText(self, value: str) -> None:
        self.entry.delete("1.0", "end")
        self.entry.insert("1.0", value)
        self.entry.update()

    def clear(self) -> None:
        self.entry.delete("1.0", "end")
        self.entry.update()
