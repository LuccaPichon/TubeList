import customtkinter

class Theme():
    """Global theme for Singleton"""
    _instance = None  # singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_theme()
        return cls._instance



    def _init_theme(self):
        # font init
        self._fontNormal = None
        self._fontTitle = None
        
        # color init
        self.bgColor = "#282A36"
        self.fgColor = "#f8f8f2"
        self.highlightBg = "#6272a4"

    @property
    def fontNormal(self):
        if self._fontNormal is None:
            self._fontNormal = customtkinter.CTkFont(family="Arial", size=15)
        return self._fontNormal

    @property
    def fontTitle(self):
        if self._fontTitle is None:
            self._fontTitle = customtkinter.CTkFont(family="Arial", size=25, weight="bold")
        return self._fontTitle
    
theme = Theme()