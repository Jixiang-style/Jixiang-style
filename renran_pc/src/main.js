// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings";
import "../static/css/reset.css";
import "../static/js/TCaptcha";

import axios from 'axios'

axios.defaults.withCredentials = false;

Vue.prototype.$axios = axios; // 把对象挂载vue中


// iconfont字体
import "../static/css/iconfont.css";
import "../static/css/iconfont.eot";

// elementUI 导入
import ElementUI from 'element-ui';
import "element-ui/lib/theme-chalk/index.css";
// 调用插件
Vue.use(ElementUI);

Vue.config.productionTip = false;
Vue.prototype.$settings = settings;

import mavonEditor from 'mavon-editor'
 import 'mavon-editor/dist/css/index.css'
Vue.use(mavonEditor);
// 注册mavon-editor组件
new Vue({
    'el': '#main'
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
