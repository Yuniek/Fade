# ##################################
# Errors
# ##################################

class FadeError(Exception):
    def __init__(self, type_, pos_start, pos_end, detail):
        self.type       = type_
        self.pos_start   = pos_start
        self.pos_end     = pos_end
        self.detail     = detail
        super().__init__(f"{self.type}:{self.detail}")

class InvalidTokenError(FadeError):
    def __init__(self, pos_start, pos_end, invalid_token):
            self.type       = "InvalidTokenError"
            self.detail     = f"Invalid token '{invalid_token}' at position {pos_start}"
            super().__init__(self.type, pos_start, pos_end, self.detail)

class InvalidSyntaxError(FadeError):
    def __init__(self, pos_start, pos_end, detail):
            self.type       = "InvalidSyntaxError"
            self.detail     = f'{detail} at position {pos_start}'
            super().__init__(self.type, pos_start, pos_end, self.detail)

class FadeRuntimeError(FadeError):
    def __init__(self, detail):
            self.type       = "RuntimeError"
            self.detail     = detail
            super().__init__(self.type, None, None, self.detail)