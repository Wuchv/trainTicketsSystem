<template>
  <div class="background">
    <div class="container">
      <div class="title">火车票售票系统</div>

      <div class="box">
        <img class="image" src="./train1.png" />

        <div class="input_box" v-if="flag === 0">
          <span class="login_title">登录账号</span>

          <div class="inner_box margin_top">
            <img class="icon" src="./account.png" />
            <input class="input" v-model="username" placeholder="输入用户名" />
          </div>

          <div class="inner_box">
            <img class="icon" src="./password.png" />
            <input class="input" placeholder="输入密码" v-model="password" type="password" />
          </div>

          <div class="link_box">
            <el-link class="link" type="info" @click="change(1)" :underline="false">忘记密码?</el-link>
            <el-link class="link" type="info" @click="change(2)" :underline="false">注册账号</el-link>
          </div>

          <el-button class="submit" type="primary" @click="onSubmit">登陆</el-button>
          <br />
        </div>

        <forget @change="change" v-else-if="flag === 1"></forget>
        <register @change="change" v-else-if="flag === 2"></register>
      </div>
    </div>

    <el-dialog title="找回密码成功" :visible.sync="dialogVisible" width="30%">
      <div style="text-align:center;font-size:18px;">
        <div style="padding:5px 0;">用户名：{{username}}</div>
        <br />
        <div>密码：{{password}}</div>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import forget from "./forget";
import register from "./register";

export default {
  name: "login",
  components: { forget, register },
  data() {
    return {
      username: "",
      password: "",
      flag: 0,
      dialogVisible: false
    };
  },
  created() {
    document.body.className = "login_bg";
  },
  methods: {
    onSubmit() {
      let _this = this;
      if (_this.username && _this.password) {
        fPost(
          "http://127.0.0.1:5000/login",
          { username: _this.username, password: _this.password },
          res => {
            console.log(res);
            if (!res.code) {
              setCookie("user_id", res.data.user_id, 60 * 60 * 60);
              setCookie("permission", res.data.permission, 60 * 60 * 60);
              _this.$router.push("/admin/tickets");
            } else {
              $msg("用户名或密码错误！", res.code, _this);
            }
          }
        );
      } else {
        $msg("请将用户名或密码填写完整", 2, _this);
      }
    },
    change(arg) {
      this.flag = arg;
      if (arguments[1] && arguments[2]) {
        this.username = arguments[1];
        this.password = arguments[2];
        this.dialogVisible = true;
      }
    }
  }
};
</script>

<style>
.login_bg {
  background-image: url("login_bg.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  background-attachment: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>


<style scoped lang="scss">
.container {
  display: flex;
  flex-direction: column;
  height: 425px;
  width: 700px;
  background-color: #fff;
  border-radius: 15px;
  margin-top: 20vh;
}

.container:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title {
  text-align: left;
  padding: 15px 30px;
  color: #fdbb10;
  font-size: 22px;
  font-family: "MicrosoftYaHei";
}

.box {
  display: flex;
  flex-direction: row;
  padding: 0 15px 15px 15px;
}

.image {
  margin: 60px 20px;
  height: 200px;
  object-fit: fill;
}

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
  margin-top: 15px;
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

.margin_top {
  margin-top: 45px;
}

.submit {
  width: 220px;
  margin-top: 50px;
  box-shadow: 0 2px 12px 0 rgba(245, 195, 25, 0.3);
  border-radius: 15px;
  border-color: #f7dc6e;
  background-image: linear-gradient(135deg, #f7dc6e 0%, #f5c319 100%);
}

.link_box {
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
}

.link {
  float: left;
  font-size: 8px;
  margin: 0 3px;
  margin-top: 5px;
}
</style>
