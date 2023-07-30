class HttpStatus:
    # 请求正常
    HTTP_200_OK = 200

    # 用户登录异常
    HTTP_418_AUTH_EXCEPT = 418

    # 用户不存在
    HTTP_419_USER_EXCEPT = 419

    # Token 过期
    HTTP_420_TOKEN_EXCEPT = 420

    # 内部参数校验失败
    HTTP_421_INNER_PARAM_EXCEPT = 421

    # 角色不存在
    HTTP_422_ROLE_NOT_EXIST = 422

    # 请求参数格式错误
    HTTP_422_QUERY_PARAM_EXCEPT = 422

    # Authentication 权限异常
    HTTP_425_AUTHENTICATION_EXCEPT = 425

    # 服务端错误
    HTTP_500_INTERNAL_SERVER_ERROR = 500

    # 角色不存在
    HTTP_600_ROLE_NOT_EXIST = 600

    # 角色不存在
    HTTP_601_ROLE_EXIST = 601
