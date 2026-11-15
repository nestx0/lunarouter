class ContextWindowExcedeed(Exception):
    """Exception raised when the context window is full"""

    def __init__(self):
        self.message = "Context window is full"
        super().__init__(self.message)
