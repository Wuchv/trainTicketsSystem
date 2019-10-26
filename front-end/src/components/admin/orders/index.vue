<template>
  <div class="container">
    <div class="order-box" v-for="(ticket,index) in orders" :key="index">
      <div class="row">
        <div>{{ticket.start_time.substring(0,10)}}</div>
        <div>{{(ticket.running_time/3600).toFixed(2)}}h</div>
        <div>{{ticket.end_time.substring(0,10)}}</div>
      </div>

      <div class="row">
        <div>{{ticket.start_time.substring(11,16)}}</div>
        <div>&#8594;</div>
        <div>{{ticket.end_time.substring(11,16)}}</div>
      </div>

      <div class="row">
        <div>{{ticket.start_station}}</div>
        <div>{{ticket.train_id}}</div>
        <div>{{ticket.end_station}}</div>
      </div>

      <div class="row" style="margin-top: 20px;">
        <div style="margin-left: 30px;">{{ticket.seat_car}}{{ticket.seat_no}}号</div>
        <div style="margin-right: 20px;">￥{{ticket.money}}</div>
        <el-button
          type="primary"
          size="mini"
          :disabled="!ticket.isFinished"
          @click="changeTicket(index)"
        >改签</el-button>
        <el-button
          style="margin-right: 20px;"
          type="primary"
          size="mini"
          :disabled="!ticket.isFinished"
          @click="returnTicket(index)"
        >退票</el-button>
      </div>
    </div>

    <el-dialog title="改签" :visible.sync="dialogchangeTicketVisible" center>
      <ticket></ticket>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogchangeTicketVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitChange">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { setTimeout } from "timers";
import ticket from "../tickets/index";

export default {
  inject: ["reload"],
  components: { ticket },
  data() {
    name: "orders";
    return {
      orders: [],
      dialogchangeTicketVisible: false,
      changeIndex: undefined
    };
  },
  created() {
    let _this = this;
    fPost(
      "http://127.0.0.1:5000/admin/getOrders",
      { user_id: getCookie("user_id") },
      res => {
        console.log(res);
        _this.orders = res.data.orders;
      }
    );
  },
  methods: {
    changeTicket(index) {
      let _this = this;
      _this.dialogchangeTicketVisible = true;
      _this.changeIndex = index;
    },
    submitChange() {
      let _this = this;
      _this.dialogchangeTicketVisible = false;
      fPost(
        "http://127.0.0.1:5000/admin/returnTicket",
        { order_id: _this.orders[_this.changeIndex].order_id },
        res => {
          console.log(res);
          $msg("改签成功", res.code, _this);
          setTimeout(() => {
            _this.reload();
          }, 1500);
        }
      );
    },
    returnTicket(index) {
      let _this = this;
      _this
        .$confirm("是否继续退票?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
        .then(() => {
          fPost(
            "http://127.0.0.1:5000/admin/returnTicket",
            { order_id: _this.orders[index].order_id },
            res => {
              console.log(res);
              $msg(res.msg, res.code, _this);
              setTimeout(() => {
                _this.reload();
              }, 1500);
            }
          );
        })
        .catch(() => {
          $msg("已取消退票", 2, _this);
        });
    }
  }
};
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
}

.order-box {
  float: left;
  width: 40%;
  display: flex;
  flex-direction: column;
  margin: 3% 5% 0 5%;
  padding: 6px 0 20px 0;
  background-color: #fff;
  border-radius: 15px;
}

.order-box:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.row {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  font-size: 16px;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  margin-top: 14px;
}
</style>