<template>
  <el-table :data="tableData" stripe style="width: 100%">
    <el-table-column label="用户名" width="120" align="center">
      <template slot-scope="scope">
        <span style="margin-left: 10px">{{ scope.row.username }}</span>
      </template>
    </el-table-column>
    <el-table-column label="真实姓名" width="100" align="center">
      <template slot-scope="scope">
        <span size="medium">{{ scope.row.rel_name }}</span>
      </template>
    </el-table-column>
    <el-table-column label="手机号" width="100" align="center">
      <template slot-scope="scope">
        <span size="medium">{{ scope.row.tel }}</span>
      </template>
    </el-table-column>
    <el-table-column label="身份证号" width="180" align="center">
      <template slot-scope="scope">
        <span size="medium">{{ scope.row.id_number }}</span>
      </template>
    </el-table-column>
    <el-table-column label="状态" width="100" align="center">
      <template slot-scope="scope">
        <span size="medium">{{ scope.row.status }}</span>
      </template>
    </el-table-column>
    <el-table-column label="操作" align="center">
      <template slot-scope="scope">
        <el-button
          size="mini"
          type="primary"
          @click="changeStatus(scope.$index, scope.row)"
          v-if="scope.row.status == '禁乘'"
        >解除禁制</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="changeStatus(scope.$index, scope.row)"
          v-else
        >禁止乘车</el-button>
        <el-button size="mini" type="danger" @click="deleteUser(scope.$index, scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: "userTable",
  inject: ["reload"],
  data() {
    return {
      tableData: []
    };
  },
  created() {
    fGet("http://127.0.0.1:5000/admin/getUsers", {}, res => {
      this.tableData = res.data.users;
    });
  },
  methods: {
    changeStatus(index, row) {
      let _this = this;
      this.$confirm("此操作将修改用户状态, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          fPost(
            "http://127.0.0.1:5000/admin/changeUserStatus",
            { user_id: row.user_id, status: row.status },
            res => {
              console.log(res);
              $msg(res.msg, res.code, this);
              setTimeout(() => {
                _this.reload();
              }, 1000);
            }
          );
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消修改"
          });
        });
    },
    deleteUser(index, row) {
      let _this = this;
      this.$confirm("此操作将删除此用户, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          fPost(
            "http://127.0.0.1:5000/admin/deleteUser",
            { user_id: row.user_id },
            res => {
              console.log(res);
              $msg(res.msg, res.code, this);
              setTimeout(() => {
                _this.reload();
              }, 1000);
            }
          );
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    }
  }
};
</script>

<style scoped>
</style>