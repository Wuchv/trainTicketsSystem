<template>
  <div>
    <h1>首页</h1>
    <el-button @click="getMsg">{{msg}}</el-button>
  </div>
</template>

<script>
export default {
  name: "index",
  data() {
    return {
      msg: "get"
    };
  },
  methods: {
    getMsg() {
      let _this = this;
      fPost(
        "http://127.0.0.1:5000/",
        { username: "a", password: "123456" },
        res => {
          console.log(res);
        }
      );
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
