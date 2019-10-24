class NetworkFullError(Exception):
    def __init__(self, message: str):
        super().__init__("Network was full and could not %s" % message)
