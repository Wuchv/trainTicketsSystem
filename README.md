# train_ticket_system

> A Vue.js and flask  project

> front-end为前端文件

> rear-end为后台文件



## 系统开发平台

开发工具：vs code ，pycham

开发语言：python，html，css，javascript

数据库：MySQL

前端框架：Vue.js

后台框架：flask



## 系统功能
在本系统中，前端和后台使用json进行数据交互，下面的每一个功能均对应着一个接口，括号中为接口的URL，具体实现可以参考源代码。

### 用户层面
+ 用户登陆（/login）
+ 用户注册（/register）
+ 找回密码（/forget）
+ 展示/修改用户信息（/getUserInfo，/updateUserInfo）

### 订单层面
+ 查询订单（/getUserOrders）
+ 添加订单（/order）
+ 修改/删除订单（/returnTicket）

### 火车层面
+ 获取火车车次（/getTrains）

+ 查询直达/换乘车票（/getDirectTickets，/getTransferTickets）

  

## 前端部署（需安装node.js)

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```


