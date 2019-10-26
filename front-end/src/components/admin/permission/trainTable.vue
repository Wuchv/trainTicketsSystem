<template>
  <el-table :data="tableData" stripe style="width: 100%">
    <el-table-column label="车次" width="120" align="center">
      <template slot-scope="scope">
        <span>{{ scope.row.train_id }}</span>
      </template>
    </el-table-column>
    <el-table-column label="类型" width="120" align="center">
      <template slot-scope="scope">
        <span size="medium">{{ scope.row.type }}</span>
      </template>
    </el-table-column>
    <el-table-column label="状态" width="120" align="center">
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
          v-if="scope.row.status == '停运'"
        >开始运行</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="changeStatus(scope.$index, scope.row)"
          v-else
        >停止运行</el-button>
        <el-button size="mini" type="danger" @click="deleteTrain(scope.$index, scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: "trainTable",
  inject: ["reload"],
  data() {
    return {
      tableData: []
    };
  },
  created() {
    fGet("http://127.0.0.1:5000/admin/getTrains", {}, res => {
      this.tableData = res.data.trains;
    });
  },
  methods: {
    changeStatus(index, row) {
      let _this = this;
      this.$confirm("此操作将修改火车运行状态, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          fPost(
            "http://127.0.0.1:5000/admin/changeTrainStatus",
            { train_id: row.train_id, status: row.status },
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
    deleteTrain(index, row) {
      let _this = this;
      this.$confirm("此操作将删除此车次, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          fPost(
            "http://127.0.0.1:5000/admin/deleteTrain",
            { train_id: row.train_id },
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