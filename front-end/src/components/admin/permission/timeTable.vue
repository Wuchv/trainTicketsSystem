<template>
  <div>
    <el-date-picker
      v-model="date"
      type="date"
      placeholder="选择日期"
      format="yyyy 年 MM 月 dd 日"
      value-format="yyyy-MM-dd"
      style="float:left;margin-bottom:15px;"
    ></el-date-picker>

    <el-button type="primary" @click="confirmed" style="float:left;margin-left:20px;">确认</el-button>

    <el-button
      type="primary"
      @click="dialogFormVisible = true"
      style="float:left;margin-left:20px;"
    >添加</el-button>

    <!-- <el-dialog title="添加时刻信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="车次" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="活动区域" :label-width="formLabelWidth">
          <el-select v-model="form.region" placeholder="请选择活动区域">
            <el-option label="区域一" value="shanghai"></el-option>
            <el-option label="区域二" value="beijing"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
      </div>
    </el-dialog>-->

    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column label="车次" width="100" align="center">
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.train_id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="停靠城市" width="120" align="center">
        <template slot-scope="scope">
          <span size="medium">{{ scope.row.city }}</span>
        </template>
      </el-table-column>
      <el-table-column label="停靠车站" width="120" align="center">
        <template slot-scope="scope">
          <span size="medium">{{ scope.row.station }}</span>
        </template>
      </el-table-column>
      <el-table-column label="到达时间" width="180" align="center">
        <template slot-scope="scope">
          <span size="medium">{{ scope.row.arrive_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="出发时间" width="180" align="center">
        <template slot-scope="scope">
          <span size="medium">{{ scope.row.leave_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="danger" @click="deleteUser(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "userTable",
  inject: ["reload"],
  data() {
    return {
      tableData: [],
      date: "",
      dialogFormVisible: false
    };
  },
  methods: {
    confirmed() {
      fPost(
        "http://127.0.0.1:5000/admin/getTimetable",
        { date: this.date },
        res => {
          this.tableData = res.data.timetable;
        }
      );
    },
    deleteUser(index, row) {
      let _this = this;
      this.$confirm("此操作将删除此记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          fPost(
            "http://127.0.0.1:5000/admin/deleteTimetable",
            {
              train_id: row.train_id,
              city: row.city,
              station: row.station,
              arrive_time: row.arrive_time
            },
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
.time-picker {
  float: left;
}
</style>