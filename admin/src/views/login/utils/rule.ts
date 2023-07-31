import {reactive} from "vue";
import type {FormRules} from "element-plus";

/** 登录校验 */
const loginRules = reactive(<FormRules>{
  username: [{
    trigger: 'blur',
    required: true,
    message: '账号不能为空！'
  },
  ],
  password: [
    {
      required:true,
      min: 5,
      max: 18,
      trigger: "blur",
      message: '密码必须为5-18位之间'
    }
  ]
});

export {loginRules};
