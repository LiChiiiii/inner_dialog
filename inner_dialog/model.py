from enum import Enum


class Model(str, Enum):
    INNER_DIALOG = "inner_dialog"
    GEMINI = "gemini"
    PALM = "palm"
    CHATGPT = "chatgpt"
    EXTRACT = "extract"
