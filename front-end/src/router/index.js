import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: "history",
  scrollBehavior(to, from, savedPosition) { //滚动条控制
    if (to.hash) {
      return {
        selector: to.hash
      }
    } else if (savedPosition) {
      return savedPosition
    } else {
      return {
        x: 0,
        y: 0
      }
    }
  },
  routes: [{
    path: '/',
    name: 'index',
    redirect: '/login',
    component: resolve => require(['@/components/index'], resolve),
    meta: {
      title: "首页",
    },
  }, {
    path: '/login',
    name: 'login',
    component: resolve => require(['@/components/login/index'], resolve),
    meta: {
      title: "登陆界面",
    },
  }, {
    path: '/admin',
    name: 'adminFrame',
    component: resolve => require(['@/components/admin/adminFrame/index'], resolve),
    meta: {
      title: "管理界面",
    },
    children: [{
      path: '/admin/userInfo',
      name: 'userInfo',
      component: resolve => require(['@/components/admin/userInfo/index'], resolve),
      meta: {
        title: "个人信息",
      },
    }, {
      path: '/admin/tickets',
      name: 'tickets',
      component: resolve => require(['@/components/admin/tickets/index'], resolve),
      meta: {
        title: "车票界面",
      },
    }, {
      path: '/admin/orders',
      name: 'orders',
      component: resolve => require(['@/components/admin/orders/index'], resolve),
      meta: {
        title: "订单界面",
      },
    }, {
      path: '/admin/permission',
      name: 'permission',
      component: resolve => require(['@/components/admin/permission/index'], resolve),
      meta: {
        title: "管理车次，权限界面",
      },
    }]
  }, {
    path: '*',
    component: resolve => require(['@/components/notfind'], resolve),
    meta: {
      title: "404"
    },
  }]
})
