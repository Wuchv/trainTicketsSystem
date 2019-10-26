<template>
  <el-container>
    <el-header>
      <el-row style="width:100%;">
        <el-col :xs="12" :sm="8" :md="6" :lg="6" :xl="6">
          <div class="title">火车票售票系统</div>
        </el-col>
        <el-col :xs="2" :sm="9" :md="13" :lg="13" :xl="6">
          <div class="grid-content"></div>
        </el-col>
        <el-col
          :xs="5"
          :sm="4"
          :md="3"
          :lg="3"
          :xl="6"
          style="display:flex;flex-direction:cloum;justify-content:center;align-items: center;height:80px;"
        >
          <router-link to="/admin/userInfo">
            <el-button type="primary">个人信息</el-button>
          </router-link>
        </el-col>
        <el-col
          :xs="5"
          :sm="3"
          :md="2"
          :lg="2"
          :xl="6"
          style="display:flex;flex-direction:cloum;justify-content:center;align-items: center;height:80px;"
        >
          <router-link to="/login">
            <el-button type="primary">退出</el-button>
          </router-link>
        </el-col>
      </el-row>
    </el-header>

    <el-container>
      <el-aside>
        <el-menu :default-active="active" class="el-menu-vertical-demo">
          <router-link to="/admin/tickets">
            <el-menu-item index="/admin/tickets" class="menu_item" style="margin-top:5vh;">
              <i class="el-icon-s-ticket"></i>
              <span slot="title">车票</span>
            </el-menu-item>
          </router-link>

          <router-link to="/admin/orders">
            <el-menu-item index="/admin/orders" class="menu_item">
              <i class="el-icon-s-order"></i>
              <span slot="title">订单</span>
            </el-menu-item>
          </router-link>

          <router-link to="/admin/permission?type=userTable" v-if="parseInt(permission)">
            <el-menu-item index="/admin/permission" class="menu_item">
              <i class="el-icon-s-tools"></i>
              <span slot="title">管理</span>
            </el-menu-item>
          </router-link>
        </el-menu>
      </el-aside>

      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: "adminFrame",
  data() {
    return {
      active: window.location.pathname,
      permission: getCookie("permission")
    };
  },
  created() {
    document.body.className = "admin_bg";
  },
  methods: {}
};
</script>

<style>
.admin_bg {
  margin: 0;
  overflow: auto;
}
</style>


<style scoped>
.el-header {
  display: flex;
  align-items: center;
  color: #333;
  line-height: 80px;
  height: 80px !important;
}

.el-aside {
  display: flex;
  justify-content: center;
  color: #333;
  text-align: center;
  width: 250px !important;
  height: 100%;
}

.el-main {
  background-color: #fafafa;
  color: #333;
  text-align: center;
  height: 80vh;
}

body > .el-container {
  margin-bottom: 40px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.title {
  display: inline;
  color: #fdbb10;
  font-size: 26px;
  font-family: "MicrosoftYaHei";
  margin-left: 14px;
}

.el-menu {
  list-style: none;
  position: relative;
  margin: 0;
  padding-left: 0;
  background-color: #ffffff;
  border: none !important;
}

.el-submenu .el-menu-item {
  padding: 0;
  min-width: 0;
}

.el-menu-item.is-active {
  color: #fff !important;
  box-shadow: 0 2px 12px 0 rgba(245, 195, 25, 0.3) !important;
  border-color: #f7dc6e !important;
  background-image: linear-gradient(
    135deg,
    #f7dc6e 0%,
    #f5c319 100%
  ) !important;
  border-radius: 4px !important;
  overflow: hidden;
}

.el-menu-item.is-active img {
  color: #fff;
  position: relative;
  left: -45px;
  -webkit-filter: drop-shadow(45px 0);
  filter: drop-shadow(45px 0);
}

.menu_item {
  margin-bottom: 2vh;
  min-width: 130px;
}

.menu_item:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
  background-color: rgba(255, 255, 255, 0) !important;
  border-radius: 4px;
}

a {
  text-decoration: none;
}
</style>

