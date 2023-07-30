class TokenAuthError(Exception):
    def __init__(self, err_desc: str = "Token登录失败"):
        self.err_desc = err_desc


class TokenExpired(Exception):
    def __init__(self, err_desc: str = "Token 已过期，请重新登录"):
        self.err_desc = err_desc


class AuthenticationError(Exception):
    def __init__(self, err_desc: str = "用户权限不足"):
        self.err_desc = err_desc
