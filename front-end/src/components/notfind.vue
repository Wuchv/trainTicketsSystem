<template>
  <center>
    <h1 style="font-size: 9rem;">404</h1>
    <h3>您访问的页面不存在,请检查或联系管理员!</h3>
    <hr />
    <div>
      <el-button type="primary" @click="$router.push('/')">首页</el-button>
      <el-button type="primary" @click="$router.back(-1)">返回</el-button>
    </div>
  </center>
</template>

<script>
export default {
  mounted() {}
};
</script>

<style scoped>
</style>
