<template>
<div id="home">
    <Header></Header>
    <div class="container">
      <div class="row">
        <div class="main">
          <!-- Banner -->
          <div class="banner">
            <el-carousel height="272px" indicator-position="none" :interval="2000">
              <el-carousel-item v-for="banner,key in banner_list" :key="item">
                <a :href="banner.link"><img :src="banner.image" alt=""></a>
              </el-carousel-item>
            </el-carousel>
          </div>
          <div id="list-container">
            <!-- 文章列表模块 -->
            <ul class="note-list">
              <li class="">
                <div class="content">
                  <a class="title" target="_blank" href="">常做此运动，让你性福加倍</a>
                  <p class="abstract">运动，是人类在发展过程中有意识地对自己身体素质的培养的各种活动 运动的方式多种多样 不仅仅是我们常知的跑步，球类，游泳等 今天就为大家介绍一种男...</p>
                  <div class="meta">
                    <span class="jsd-meta">
                      <img src="/static/image/paid1.svg" alt=""> 4.8
                    </span>
                    <a class="nickname" target="_blank" href="">上班族也健身</a>
                    <a target="_blank" href="">
                      <img src="/static/image/comment.svg" alt=""> 4
                    </a>
                    <span><img src="/static/image/like.svg" alt=""> 31</span>
                  </div>
                </div>
              </li>
              <li class="have-img">
                <a class="wrap-img" href="" target="_blank">
                  <img class="img-blur-done" src="/static/image/10907624-107943365323e5b9.jpeg" />
                </a>
                <div class="content">
                  <a class="title" target="_blank" href="">“不耻下问”，正在毁掉你的人生</a>
                  <p class="abstract">
                    在过去，遇到不懂的问题，你不耻下问，找个人问问就行；在现在，如果你还这么干，多半会被认为是“搜商低”。 昨天，35岁的表姐把我拉黑了。 表姐是医...
                  </p>
                  <div class="meta">
                    <span class="jsd-meta">
                      <img src="/static/image/paid1.svg" alt=""> 6.7
                    </span>
                    <a class="nickname" target="_blank" href="">_飞鱼</a>
                    <a target="_blank" href="">
                      <img src="/static/image/comment.svg" alt=""> 33
                    </a>
                    <span><img src="/static/image/like.svg" alt=""> 113</span>
                    <span><img src="/static/image/shang.svg" alt=""> 2</span>
                  </div>
                </div>
              </li>
            </ul>
            <!-- 文章列表模块 -->
          </div>
        <a href="" class="load-more">阅读更多</a></div>
        <div class="aside">
          <!-- 推荐作者 -->
          <div class="recommended-author-wrap">
            <!---->
            <div class="recommended-authors">
              <div class="title">
                <span>推荐作者</span>
                <a class="page-change"><img class="icon-change" src="/static/image/exchange-rate.svg" alt="">换一批</a>
              </div>
              <ul class="list">
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>

              </ul>
              <a href="" target="_blank" class="find-more">查看全部 ></a>
              <!---->
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
  import Header from "./common/Header";
  import Footer from "./common/Footer";
  export default {
      name:"Home",
      data(){
          return {
            banner_list: [],  // 轮播图广告
          }
      },
      components:{
        Header,
        Footer,
      },
      created(){
         this.get_banner();
      },
      methods:{
          get_banner(){
              // 获取轮播广告
              this.$axios.get(`${this.$settings.Host}/banner/`).then(response=>{
                  this.banner_list = response.data;
              }).catch(error=>{
                  this.$message.error("无法获取服务端的轮播广告信息!");
              })
          }
      }
  }
</script>



<style>
.banner img{
  max-height: 100%;
  max-width: 100%;
}
</style>
