class GeetestException(Exception):

    def __init__(self, err_desc: str = None):
        self.err_desc = err_desc
