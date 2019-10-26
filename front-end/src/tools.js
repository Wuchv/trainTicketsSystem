//常用函数

//url请求

//进度条，使用 npm install nprogress 命令安装
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

/**
 * @desc 发送post请求
 * @param url 请求地址（不包括服务器地址）
 * @param data 要携带的数据
 * @param fn 回调函数
 */
const fPost = function (url, data, fn) {
  //进度条开始
  NProgress.start();

  axios.post(url, data, {
      method: 'post',
      baseURL: process.env.API_ROOT,
      withCredentials: true,
    })
    .then(function (res) {
      // 根据返回码进行一些操作
      // if (res.data.code == 0) {
      //   console.log(res.data.msg);
      //   return false;
      // }
      //进度条结束
      NProgress.done();
      fn(res.data);
    })
    .catch(function (error) {
      NProgress.done();
      fn({
        code: 1,
        data: [],
        msg: "api 请求失败"
      });
      console.log(error);
    });
};

/**
 * @desc 发送get请求
 * @param url 请求地址（不包括服务器地址）
 * @param data 要携带的数据
 * @param fn 回调函数
 */
const fGet = function (url, data, fn) {
  NProgress.start();

  axios.get(url, {
      params: data
    }, {
      method: 'get',
      baseURL: process.env.API_ROOT,
      withCredentials: true,
    })
    .then(function (res) {
      // 根据返回码进行一些操作
      // if (res.data.code == 0) {
      //   console.log(res.data.msg);
      //   return false;
      // }
      NProgress.done();
      fn(res.data);
    })
    .catch(function (error) {
      NProgress.done();
      fn({
        code: 1,
        data: [],
        msg: "api 请求失败"
      });
      console.log(error);
    });
};

//cookie操作

/**
 * @desc 设置cookie
 * @param cname 名称
 * @param cvalue 值
 * @param expire 过期时间
 */
const setCookie = function (cname, cvalue, expire) {
  let d = new Date();
  d.setTime(d.getTime() + (expire * 1000));
  let expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires + ";path=/";
};

/**
 * @desc 获取cookie
 * @param cname
 * @returns {string}
 */
const getCookie = function (cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') c = c.substring(1);
    if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
  }
  return "";
};

/**
 * @desc 清除cookie
 * @param name
 */
const clearCookie = function (name) {
  setCookie(name, "", -1);
};

//数组操作

/**
 * @desc 数组去重
 * @param arr 去重数组
 * @returns {Array} 去重后的数组
 */
const arrayDeduplication = (arr) => {
  let newArr = arr.filter((element, index, self) => {
    return self.indexOf(element) === index;
  });
  return newArr
}

/**
 * @desc 计算数组元素出现次数
 * @param arr
 * @returns {数组元素:次数}
 */
const calArrayNum = (arr) => {
  //reduce也可以用来计算数组的累加，累乘
  let result = arr.reduce((pre, cur) => {
    if (cur in pre) {
      pre[cur]++
    } else {
      pre[cur] = 1
    }
    return pre
  }, {})
  return result
}

//日期操作

/**
 * @desc 获取当前时间，格式YYYY-MM-DD
 * @param date 初始化时间对象
 */
const getToday = function (date) {
  let seperator1 = "-";
  let year = date.getFullYear();
  let month = date.getMonth() + 1;
  let strDate = date.getDate();
  if (month >= 1 && month <= 9) {
    month = "0" + month;
  }
  if (strDate >= 0 && strDate <= 9) {
    strDate = "0" + strDate;
  }
  let currentdate = year + seperator1 + month + seperator1 + strDate;
  return currentdate;
};

/**
 * @desc 消息提示
 * @desc 基于elementUI
 * @desc 5秒后消失
 * @param msg 提示内容
 * @param type 0，成功，默认；1失败；2，警告
 */
const notification = function (msg = "操作成功", type = 0, context) {

  let map = {
    0: 'success',
    1: 'error',
    2: 'warning',
  };

  context.$message({
    showClose: true,
    message: msg,
    type: map[type],
    duration: 1000 * 5,
  });
};

/**
 * @desc 函数防抖，就是指触发事件后在 n 秒内函数只能执行一次，如果在 n 秒内又触发了事件，则会重新计算函数执行时间。
 * @param func 函数
 * @param wait 延迟执行毫秒数
 * @param immediate true 表立即执行，false 表非立即执行
 */
function debounce(func, wait, immediate) {
  let timeout;

  return function () {
    let context = this;
    let args = arguments;

    if (timeout) clearTimeout(timeout);
    if (immediate) {
      var callNow = !timeout;
      timeout = setTimeout(() => {
        timeout = null;
      }, wait)
      if (callNow) func.apply(context, args)
    } else {
      timeout = setTimeout(function () {
        func.apply(context, args)
      }, wait);
    }
  }
}

/**
 * @desc 函数节流，就是指连续触发事件但是在 n 秒中只执行一次函数。
 * @param func 函数
 * @param wait 延迟执行毫秒数
 */
function throttle(func, wait) {
  let previous = 0;
  return function () {
    let now = Date.now();
    let context = this;
    let args = arguments;
    if (now - previous > wait) {
      func.apply(context, args);
      previous = now;
    }
  }
}

export {
  fPost,
  fGet,
  setCookie,
  getCookie,
  clearCookie,
  arrayDeduplication,
  calArrayNum,
  getToday,
  notification,
  debounce,
  throttle
}
