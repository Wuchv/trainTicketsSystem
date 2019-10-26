//放置全局的js代码

import router from "@/router/";
/**
 * Nprogress.js
 * http://ricostacruz.com/nprogress/
 */
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

//路由拦截器
router.beforeEach((to, from, next) => {

  // 开始进度条
  NProgress.start();

  //网页标题
  if (to.meta.title) {
    document.title = to.meta.title
  } else {
    document.title = webTitle
  }


  //后台必须登录
  if (to.path.indexOf("/admin") !== -1 && to.path.indexOf("/login") === -1 && !getCookie('token')) {

    alert('请先登录');
    // 跳转到登录
    next({
      path: '/login',
      query: {redirect: to.fullPath}
    });

    return false;
  }


  // 以下情况不做拦截
  if (!to.matched.some(record => record.meta.checkLogin)) {
    next(); // 确保一定要调用 next()
    return false;
  }

  //验证后否登录
  if (getCookie('token')) {
    next();
    return false;
  }

  alert("请先登录");
  setTimeout(function () {
    // 结束滚动条
    NProgress.done();

    // 跳转到登录
    next({
      path: '/login',
      query: {redirect: to.fullPath}
    });
  }, 2000);

});

router.afterEach(transition => {
  NProgress.done();
});
