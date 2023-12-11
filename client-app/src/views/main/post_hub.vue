<template>
  <div>
    <el-dialog v-model="dialogVisible" title="新建帖子">
      <el-form :model="newPost" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="newPost.title"></el-input>
        </el-form-item>
        <el-form-item label="内容">
          <mavon-editor class="markdown" :value="newPost.content" v-model="newPost.content"
            :scrollStyle="mavon_config.scrollStyle" :toolbars="mavon_config.toolbars" :subfield="mavon_config.subfield"
            placeholder="请输入内容" style="height: 200px;width: 100%;margin-bottom: 10px" @imgAdd="img_add" />
          <!--<el-input type="textarea" v-model="newPost.content"></el-input>-->
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" style="display: flex; justify-content: flex-end;">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="savePost">确 定</el-button>
      </div>
    </el-dialog>
  </div>
  <div style="width: 1000px;position:absolute;margin: auto;top: 0;left: 0;bottom: 0;right: 0;">
      <el-card style="margin-top: 20px;display: flex; align-items: center; margin-bottom: 20px; width: 100%;">
        <h1 style="width: auto;">{{ this.title }}</h1>
        <div style="display: flex; align-items: center; width: 960px;">
          <el-input v-model="searchKeyword" placeholder="输入关键字搜索" style="display: inline-block; width: 190px;" />
          <el-button plain type="primary" @click="searchPosts">
            <el-icon><Search /></el-icon>
          </el-button>
          <span style="position: absolute; right:20px;">
            <el-button plain type="primary" @click="searchMyPosts">查看我的帖子</el-button>
            <el-button type="primary" @click="showDialog" color="#626aef">
              <el-icon><Plus /></el-icon>
              <span> 新建帖子</span>
            </el-button>
          </span>
        </div>
      </el-card>



    <div class="post-list">
      <post v-for="post in posts" :key="post.pid" :post="post" />
    </div>
    <el-pagination background layout="prev, pager, next" :page-count="totalPages" @current-change="loadPage" style="margin-top: 10px;"/>
  </div>
</template>
    
<script>
import post from "@/views/main/post_component/post.vue";
import { upload_picture } from "@/views/main/api";
import axios from 'axios';
import { ref } from "vue";
import userStateStore from "@/store";
export default {
  name: "post_hub",
  components: {
    post
  },
  data() {
    return {
      title: "全部帖子",
      posts: [],
      pageNo: 1,
      pageSize: 5,
      totalPosts: 0,
      searchKeyword: '',
      state: 'all',
      newPost: {}
    };
  },
  setup() {
    const dialogVisible = ref(false);
    const mavon_config = ref({
      scrollStyle: true,
      toolbars: {
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        strikethrough: false, // 中划线
        mark: false, // 标记
        superscript: true, // 上角标
        subscript: true, // 下角标
        quote: true, // 引用
        ol: true, // 有序列表
        ul: true, // 无序列表
        link: true, // 链接
        imagelink: true, // 图片链接
        code: true, // code
        table: true, // 表格
        fullscreen: false, // 全屏编辑
        readmodel: false, // 沉浸式阅读
        htmlcode: false, // 展示html源码
        help: false, // 帮助
        undo: true, // 上一步
        redo: true, // 下一步
        trash: true, // 清空
        save: true, // 保存（触发events中的save事件）
        navigation: false, // 导航目录
        alignleft: true, // 左对齐
        aligncenter: true, // 居中
        alignright: true, // 右对齐
        subfield: false, // 单双栏模式
        preview: true, // 预览
      }
    }
    )
    const totalPages = ref(1)
    return {
      dialogVisible,
      mavon_config,
      totalPages
    }
  },
  mounted() {
    this.loadPosts();
  },
  methods: {
    img_add(pos, file) {
      let form_data = new FormData
      form_data.append('image', file)
      upload_picture(form_data).then(
        (res) => {
          let content = this.newPost.content
          let name = file.name
          // 第二步.将返回的url替换到文本原位置![...](0) -> ![...](url)  这里是必须要有的
          if (content.includes(name)) {
            let oStr = `(${pos})`
            let nStr = `(${res.img_url})`
            let index = content.indexOf(oStr)
            let str = content.replace(oStr, '')
            let insertStr = (soure, start, newStr) => {
              return soure.slice(0, start) + newStr + soure.slice(start)
            }
            this.newPost.content = insertStr(str, index, nStr)
          }
        }
      )
    },
    loadPosts() {
      // 发送 POST 请求，获取帖子数据和总数量
      const requestData = {
        page_no: this.pageNo,
        page_size: this.pageSize
      };
      axios.post('/post_hub', requestData)
        .then(response => {
          // 处理返回的帖子数据和总数量
          this.posts = response.data.posts;
          this.totalPosts = response.data.total;
          this.totalPages = Math.ceil(response.data.total / this.pageSize)
        })
        .catch(error => {
          console.error('加载帖子失败', error);
        });
    },
    loadPage(page) {
      this.pageNo = page
      switch (this.state) {
        case "all": this.loadPosts(); break;
        case "search": this.searchMyPosts(); break;
        case "my": this.searchMyPosts(); break;
      }
    },
    searchPosts() {
      if (this.searchKeyword == "") {
        this.pageNo = 1;
        this.loadPosts();
        this.title = "全部帖子";
        this.state = "all"
        return;
      }
      if (this.state != "search") {
        this.state = "search";
        this.pageNo = 1;
        this.title = this.searchKeyword + "搜索结果";
      }
      const requestData = {
        page_no: this.pageNo,
        page_size: this.pageSize,
        key_word: this.searchKeyword
      };
      axios.post('/search_post', requestData)
        .then(response => {
          // 处理返回的帖子数据和总数量
          this.posts = response.data.posts;
          this.totalPosts = response.data.total;
          this.totalPages = Math.ceil(response.data.total / this.pageSize)
          this.title = this.searchKeyword + "的搜索结果";
          this.searchKeyword = '';
        })
        .catch(error => {
          console.error('加载帖子失败', error);
        });
    },
    searchMyPosts() {
      if (this.state != "my") {
        this.state = "my";
        this.pageNo = 1;
        this.title = "我的帖子";
      }
      const store = userStateStore();
      const requestData = {
        page_no: this.pageNo,
        page_size: this.pageSize,
        uid: store.getUserId,
      };
      axios.post('/get_user_post', requestData)
        .then(response => {
          // 处理返回的帖子数据和总数量
          this.posts = response.data.posts;
          this.totalPosts = response.data.total;
          this.totalPages = Math.ceil(response.data.total / this.pageSize)
          this.title = "我的帖子";
        })
        .catch(error => {
          console.error('加载帖子失败', error);
        });
    },
    showDialog() {
      this.dialogVisible = true;
    },
    savePost() {
      // 这里可以添加保存帖子的逻辑，比如发送到后端API
      console.log('保存帖子', this.post);
      this.dialogVisible = false;
      const store = userStateStore();
      const requestData = {
        title: this.newPost.title,
        content: this.newPost.content,
        uid: store.getUserId,
      };
      axios.post('/create_post', requestData)
        .then(response => {
          // 处理返回的帖子数据和总数量
          console.log(response)
        })
        .catch(error => {
          console.error('加载帖子失败', error);
        });
    }
  },
};
</script>
<style scoped>
.post-list {
  display: flex;
  /* 使用flex布局 */
  flex-direction: column;
  /* 设置主轴方向为纵向 */
  gap: 20px;
  /* 设置卡片之间的间距为20px */
}

.pagination {
  margin-top: 20px;
}

.pagination button {
  margin-right: 5px;
}

.pagination button.active {
  font-weight: bold;
}
</style>
  