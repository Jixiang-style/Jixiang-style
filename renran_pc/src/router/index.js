import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home'
import Login from "../components/Login";
import Register from "../components/Register"
import QQCallBack from "../components/QQCallBack";
import Writer from "../components/Writer";
import PostArticle from "../components/PostArticle";
import Article from "../components/Article";
import Wallet from "../components/Wallet";

// import axios from 'axios'
// Vue.config.axios = axios

Vue.use(Router)

export default new Router({
  mode: "history",
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      name: "Home",
      path: "/home",
      component: Home,
    },
    {
      name: "Login",
      path: "/login",
      component: Login,
    },
    {
      name: "Register",
      path: "/register",
      component: Register,
    }, {
      path: "/oauth_callback.html",   // 改成自己注册QQ登录时的地址,不是一定要.html,只是我当初不小心加了而已,
      name: 'QQCallBack',
      component: QQCallBack,
    }, {
      name: "Writer",
      path: "/writer",
      component: Writer,
    }, {
      name: "PostArticle",
      path: "/post",
      component: PostArticle,
    },
    {
      name: "Article",
      path: "/article/:id",
      component: Article,
    },
    {
      name: "Wallet",
      path: "/wallet",
      component: Wallet,
    },
  ]
})
