class HttpStatus:
    HTTP_200_OK = 200
    # 参数错误
    HTTP_400_BAD_REQUEST = 400
    # 登录失败
    HTTP_401_UNAUTHORIZED = 401
    # 未找到
    HTTP_404_NOT_FOUND = 404
    # 没有权限
    HTTP_403_FORBIDDEN_EXCEPT = 403
    # 请求被拒绝
    HTTP_406_NOT_ACCEPTABLE = 406
    # 请求超时
    HTTP_408_REQUEST_TIMEOUT = 408
    # 用户已存在
    HTTP_409_CONFLICT = 409
    # 受权异常
    HTTP_407_AUTH_EXCEPT = 407
    # 用户不存在
    HTTP_419_USER_EXCEPT = 419
    # 服务器错误
    HTTP_500_INTERNAL_SERVER_ERROR = 500

