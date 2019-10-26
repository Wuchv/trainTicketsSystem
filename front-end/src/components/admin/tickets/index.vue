<template>
  <div>
    <div class="choose-box">
      <el-cascader placeholder="起点" :options="options" v-model="start_city" filterable></el-cascader>
      <el-cascader placeholder="终点" :options="options" v-model="end_city" filterable></el-cascader>
      <el-date-picker
        v-model="date"
        type="date"
        placeholder="选择日期"
        format="yyyy 年 MM 月 dd 日"
        value-format="yyyy-MM-dd"
      ></el-date-picker>
      <el-button type="primary" @click="confirmed">确认</el-button>
    </div>

    <el-table
      :data="tableData"
      class="table"
      :row-class-name="tableRowClassName"
      row-key="train_id"
      :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
    >
      <el-table-column label="车次" width="100" align="center">
        <template #default="{row}">
          <span>{{ row.train_id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="出发站/时间" width="150" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.start_station }}/{{ scope.row.start_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="运行时长" width="120" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.running_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="到站/时间" width="120" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.end_station }}/{{ scope.row.end_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="坐席/参考价/余票" width="180" align="center">
        <template slot-scope="scope">
          <span
            v-if="scope.row.seat_1"
          >{{ scope.row.seat_1.seat_type }}/{{ scope.row.seat_1.price }}/{{ scope.row.seat_1.residual_ticket }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button
            v-if="(scope.row.seat_1 && scope.row.isDirect) || (scope.row.train_id.indexOf('/') != -1)"
            type="primary"
            size="mini"
            @click="order(scope.row, scope.row.seat_1)"
            :disabled="scope.row.seat_1 && !scope.row.seat_1.residual_ticket"
          >预订</el-button>
          <el-radio
            v-model="radio[scope.row.train_id]"
            :label="scope.row.seat_1"
            v-if="!scope.row.isDirect && (scope.row.train_id.indexOf('/') === -1)"
            @change="addSeats(scope.row,scope.row.seat_1, scope.row.index)"
            :disabled="scope.row.seat_1 && !scope.row.seat_1.residual_ticket"
          >&ensp;</el-radio>
        </template>
      </el-table-column>
      <el-table-column label="坐席/参考价/余票" width="180" align="center">
        <template slot-scope="scope">
          <span
            v-if="scope.row.seat_2"
          >{{ scope.row.seat_2.seat_type }}/{{ scope.row.seat_2.price }}/{{ scope.row.seat_2.residual_ticket }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button
            v-if="scope.row.seat_2 && scope.row.isDirect"
            type="primary"
            size="mini"
            @click="order(scope.row, scope.row.seat_2)"
            :disabled="scope.row.seat_2 && !scope.row.seat_2.residual_ticket"
          >预订</el-button>
          <el-radio
            v-model="radio[scope.row.train_id]"
            :label="scope.row.seat_2"
            v-if="!scope.row.isDirect && (scope.row.train_id.indexOf('/') === -1)"
            @change="addSeats(scope.row,scope.row.seat_2, scope.row.index)"
            :disabled="scope.row.seat_2 && !scope.row.seat_2.residual_ticket"
          >&ensp;</el-radio>
        </template>
      </el-table-column>
      <el-table-column label="坐席/参考价/余票" width="180" align="center">
        <template slot-scope="scope">
          <span
            v-if="scope.row.seat_3"
          >{{ scope.row.seat_3.seat_type }}/{{ scope.row.seat_3.price }}/{{ scope.row.seat_3.residual_ticket }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button
            v-if="scope.row.seat_3 && scope.row.isDirect"
            type="primary"
            size="mini"
            @click="order(scope.row, scope.row.seat_3)"
            :disabled="scope.row.seat_3 && !scope.row.seat_3.residual_ticket"
          >预订</el-button>
          <el-radio
            v-model="radio[scope.row.train_id]"
            :label="scope.row.seat_3"
            v-if="!scope.row.isDirect && (scope.row.train_id.indexOf('/') === -1)"
            @change="addSeats(scope.row, scope.row.seat_3, scope.row.index)"
            :disabled="scope.row.seat_3 && !scope.row.seat_3.residual_ticket"
          >&ensp;</el-radio>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { provinceAndCityData, CodeToText } from "element-china-area-data";

export default {
  name: "tickets",
  data() {
    return {
      options: provinceAndCityData,
      start_city: "",
      end_city: "",
      date: "",
      tableData: [],
      transferSeats: [],
      radio: [],
      seats: []
    };
  },
  methods: {
    confirmed() {
      let _this = this;
      let start_city =
        CodeToText[this.start_city[0]] + "/" + CodeToText[this.start_city[1]];
      let end_city =
        CodeToText[this.end_city[0]] + "/" + CodeToText[this.end_city[1]];

      //获取车票
      fPost(
        "http://127.0.0.1:5000/admin/getTickets",
        { start_city: start_city, end_city: end_city, date: _this.date },
        res => {
          console.log(res.data);
          _this.tableData = res.data;
        }
      );
    },
    tableRowClassName({ row, rowIndex }) {
      if (!row.isDirect) {
        return "warning-row";
      } else {
        return "success-row";
      }
      return "";
    },
    order(row, seat) {
      let _this = this;
      let order = {};
      order["user_id"] = getCookie("user_id");
      order["date"] = _this.date;
      _this
        .$confirm("是否继续买票?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
        .then(() => {
          if (row.seat_2 && row.seat_3) {
            order["isDirect"] = true;
            order["detail"] = row;
            order["seat"] = seat;
          } else {
            if (_this.seats[0] && _this.seats[1]) {
              order["isDirect"] = false;
              order["fOrder"] = _this.seats[0];
              order["sOrder"] = _this.seats[1];
            } else {
              $msg("请选择座位类型", 1, _this);
              return;
            }
          }
          fPost("http://127.0.0.1:5000/admin/order", { order: order }, res => {
            console.log(res.data);
            $msg(res.msg, res.code, _this);

            let start_city =
              CodeToText[_this.start_city[0]] +
              "/" +
              CodeToText[_this.start_city[1]];
            let end_city =
              CodeToText[_this.end_city[0]] +
              "/" +
              CodeToText[_this.end_city[1]];
            fPost(
              "http://127.0.0.1:5000/admin/getTickets",
              { start_city: start_city, end_city: end_city, date: _this.date },
              res => {
                console.log(res.data);
                _this.tableData = res.data;
              }
            );
          });
        })
        .catch(() => {
          $msg("已取消买票", 2, _this);
        });
    },
    addSeats(row, seat, index) {
      row["seat"] = seat;
      this.seats[index] = row;
    }
  }
};
</script>

<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>


<style scoped>
.choose-box {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  margin-top: 2vh;
}

.table {
  width: 95%;
  margin: 5vh 2.5%;
  border-radius: 10px;
}

.table:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
</style>

