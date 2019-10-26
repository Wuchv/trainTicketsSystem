// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import * as tools from './tools'

window.tools = tools;

Vue.config.productionTip = false

/**
 * axios
 * http://www.mamicode.com/info-detail-2219622.html
 */
import axios from "axios";
window.axios = axios;
axios.defaults.withCredentials = true;

// 公共方法
import './app/funcitons'

//引入第三方类库
/**
 * ElementUI
 * http://element-cn.eleme.io/#/zh-CN/component/installation/
 */
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './app/element-variables.scss';
Vue.use(ElementUI);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {
    App
  },
  render: h => h(App),
  template: '<App/>'
}).$mount('#app');
