<template>
  <div class="container">
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
      <el-tab-pane label="用户管理" name="userTable">
        <user-table></user-table>
      </el-tab-pane>
      <el-tab-pane label="车次管理" name="trainTable">
        <train-table></train-table>
      </el-tab-pane>
      <el-tab-pane label="时刻表" name="timeTable">
        <time-table></time-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import userTable from "./userTable";
import trainTable from "./trainTable";
import timeTable from "./timeTable";
import merge from "webpack-merge";

export default {
  name: "permission",
  components: { userTable, trainTable, timeTable },
  data() {
    return {
      activeName: this.$route.query.type
    };
  },
  methods: {
    handleClick(tab, event) {
      this.$router.push({
        query: merge(this.$route.query, { type: tab.name })
      });
    }
  }
};
</script>

<style scoped>
.container {
  width: 90%;
  margin: 20px 5%;
}
</style>