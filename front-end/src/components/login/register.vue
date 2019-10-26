<template>
  <div class="input_box">
    <span class="login_title">注册账号</span>

    <div class="inner_box margin_top">
      <img class="icon" src="./account.png" />
      <input class="input" v-model="username" placeholder="请输入用户名" />
    </div>

    <div class="inner_box">
      <img class="icon" src="./password.png" />
      <input class="input" placeholder="请输入密码" v-model="password" type="password" />
    </div>

    <div class="inner_box">
      <img class="icon" src="./tel.png" />
      <input
        class="input"
        placeholder="请输入手机号"
        v-model="tel"
        oninput="value=value.replace(/[^\d]/g,'')"
      />
    </div>

    <div class="radio_box">
      <el-radio v-model="radio" label="0">普通用户</el-radio>
      <el-radio v-model="radio" label="1">管理员</el-radio>
    </div>

    <el-button class="submit" type="primary" @click="onSubmit">确认</el-button>

    <div class="link_box">
      <el-link class="link" type="info" @click="back(0)" :underline="false">返回</el-link>
    </div>
  </div>
</template>


<script>
export default {
  name: "register",
  data() {
    return {
      username: "",
      password: "",
      tel: "",
      value: "",
      radio: "0"
    };
  },
  methods: {
    onSubmit() {
      let _this = this;
      if (_this.username && _this.tel && _this.password) {
        fPost(
          "http://127.0.0.1:5000/register",
          {
            username: _this.username,
            password: _this.password,
            tel: _this.tel,
            radio: _this.radio
          },
          res => {
            console.log(res);
            if (!res.code) {
              $msg(res.msg, 0, _this);
              _this.back(0);
            } else {
              $msg(res.msg + "，手机号或者用户名已被注册", 1, _this);
            }
          }
        );
      } else {
        $msg("请将信息填写完整", 2, _this);
      }
    },
    back(arg) {
      this.$emit("change", arg);
    }
  }
};
</script>

<style scoped lang="scss">
.input_box {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 65px;
}

.login_title {
  font-size: 28px;
  color: #fdbb10;
}

.inner_box {
  display: flex;
  flex-direction: row;
  height: 35px;
  align-items: center;
  justify-content: center;
  padding: 3px;
  margin-top: 10px;
  border-bottom: 1px solid #dcdfe6;
}

.icon {
  width: 18px;
  height: 18px;
}

.input {
  border: none;
  -webkit-appearance: none;
  background-color: #fff;
  background-image: none;
  border: none;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  color: #606266;
  display: inline-block;
  font-size: inherit;
  height: 40px;
  line-height: 40px;
  outline: 0;
  padding: 0 15px;
  -webkit-transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  width: 100%;
}

.el-input__inner {
  -webkit-appearance: none;
  background-color: #ffffff;
  background-image: none;
  border-radius: 4px;
  border: 1px solid rgb(36, 85, 201) !important;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  color: #606266;
  display: inline-block;
  font-size: inherit;
  height: 40px;
  line-height: 40px;
  outline: none;
  padding: 0 15px;
  -webkit-transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  width: 100%;
}

.margin_top {
  margin-top: 25px;
}

.submit {
  width: 220px;
  margin-top: 30px;
  box-shadow: 0 2px 12px 0 rgba(245, 195, 25, 0.3);
  border-radius: 15px;
  border-color: #f7dc6e;
  background-image: linear-gradient(135deg, #f7dc6e 0%, #f5c319 100%);
}

.link_box {
  display: flex;
  flex-direction: row-reverse;
  width: 100%;
}

.link {
  font-size: 8px;
  margin: 0 3px;
  margin-top: 5px;
}

.radio_box {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  width: 100%;
  margin-top: 20px;
}
</style>
