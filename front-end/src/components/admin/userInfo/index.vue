<template>
  <div class="box">
    <el-card class="box-card" shadow="hover">
      <div style="font-weight:600;margin-top:1.5vh;display:inline-block;">个人信息</div>

      <el-button v-if="!isEdit" class="edit-button" type="primary" @click="isEdit = true">编辑信息</el-button>
      <el-button v-if="isEdit" class="edit-button" type="primary" @click="edited">完成编辑</el-button>

      <div class="msg_box">
        <div class="detail">
          <span style="margin-top:5vh;">用户名：</span>
          <span style="margin-top:5vh;">真实姓名：</span>
          <span style="margin-top:5vh;">性别：</span>
          <span style="margin-top:5vh;">联系电话：</span>
          <span style="margin-top:5vh;">证件类别：</span>
          <span style="margin-top:5vh;">证件号码：</span>
          <span style="margin-top:5vh;">我的密码：</span>
        </div>

        <div v-if="!isEdit" class="detail">
          <span style="margin-top:5vh;">{{userInfo.username}}</span>
          <span v-if="userInfo.rel_name" style="margin-top:5.2vh;">{{userInfo.rel_name}}</span>
          <span v-if="!userInfo.rel_name" style="margin-top:5.2vh;">空</span>
          <span v-if="userInfo.sex" style="margin-top:5.2vh;">{{userInfo.sex}}</span>
          <span v-if="!userInfo.sex" style="margin-top:5.2vh;">空</span>
          <span style="margin-top:5.2vh;">{{userInfo.tel}}</span>
          <span
            v-if="userInfo.type_of_certificate"
            style="margin-top:5vh;"
          >{{userInfo.type_of_certificate}}</span>
          <span v-if="!userInfo.type_of_certificate" style="margin-top:5vh;">空</span>
          <span v-if="userInfo.id_number" style="margin-top:5vh;">{{userInfo.id_number}}</span>
          <span v-if="!userInfo.id_number" style="margin-top:5vh;">空</span>
          <div>
            <el-input
              style="margin-top:4vh;width:10vw;margin-right:3vw;"
              v-model="userInfo.password"
              show-password
            ></el-input>
          </div>
        </div>

        <div v-if="isEdit" class="detail">
          <el-input style="margin-top:4vh;width:10vw;margin-right:3vw;" v-model="userInfo.username"></el-input>
          <el-input style="margin-top:2.4vh;width:10vw;margin-right:3vw;" v-model="userInfo.rel_name"></el-input>
          <el-input style="margin-top:2.4vh;width:10vw;margin-right:3vw;" v-model="userInfo.sex"></el-input>
          <el-input style="margin-top:2.4vh;width:10vw;margin-right:3vw;" v-model="userInfo.tel"></el-input>
          <el-input
            style="margin-top:2.4vh;width:10vw;margin-right:3vw;"
            v-model="userInfo.type_0f_certificate"
          ></el-input>
          <el-input
            style="margin-top:2.4vh;width:10vw;margin-right:3vw;"
            v-model="userInfo.id_number"
          ></el-input>
          <div>
            <el-input
              style="margin-top:4vh;width:10vw;margin-right:3vw;"
              v-model="userInfo.password"
              show-password
            ></el-input>
          </div>
        </div>
      </div>
    </el-card>

    <!-- <el-dialog title="修改密码" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="原密码" :label-width="formLabelWidth">
          <el-input v-model="form.password" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="新密码" :label-width="formLabelWidth">
          <el-input v-model="form.newPassword" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="确认密码" :label-width="formLabelWidth">
          <el-input v-model="form._newPassword" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="changePassword">确 定</el-button>
      </div>
    </el-dialog>-->
  </div>
</template>

<script>
export default {
  name: "userInfo",
  data() {
    return {
      isEdit: false,
      userInfo: {
        username: "",
        rel_name: "",
        tel: "",
        password: "",
        sex: "",
        type_of_certificate: "",
        id_number: ""
      },
      // dialogFormVisible: false,
      // form: {
      //   password: "",
      //   newPassword: "",
      //   _newPassword: ""
      // },
      formLabelWidth: "120px"
    };
  },
  created() {
    let _this = this;

    //根据id获取个人信息
    fPost(
      "http://127.0.0.1:5000/admin/getUserInfo",
      { user_id: getCookie("user_id") },
      res => {
        let data = res.data;
        console.log(res.data);
        _this.userInfo.username = data.username;
        _this.userInfo.rel_name = data.rel_name;
        _this.userInfo.tel = data.tel;
        _this.userInfo.password = data.password;
        _this.userInfo.type_of_certificate = data.type_of_certificate;
        _this.userInfo.id_number = data.id_number;
        _this.userInfo.sex = data.sex;
      }
    );
  },
  methods: {
    // changePassword() {
    //   let _this = this;
    //   _this.dialogFormVisible = false;
    //   console.log(_this.form);
    //   //根据原密码修改密码
    // },
    edited() {
      let _this = this;
      //更新信息
      fPost(
        "http://127.0.0.1:5000/admin/updateUserInfo",
        { user_id: getCookie("user_id"), userInfo: _this.userInfo },
        res => {
          $msg(res.msg, res.code, _this);
          _this.isEdit = false;
        }
      );
    }
  }
};
</script>

<style scoped>
.box {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
}

.box-card {
  width: 70%;
  text-align: left;
  margin-top: 5vh;
  padding: 3vmin 8vmin 5vmin 8vmin;
}

.msg_box {
  width: 100%;
  display: flex;
  flex-direction: row;
}

.detail {
  display: flex;
  flex-direction: column;
  text-align: left;
  width: 50%;
}

.edit-button {
  float: right;
}
</style>


