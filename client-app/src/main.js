import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from "axios";
import locale from 'element-plus/es/locale/lang/zh-cn'
import ElementPlus from 'element-plus'
import {createPinia} from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import Prism from 'prismjs';
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';

axios.defaults.timeout = 100000;

import hljs from 'highlight.js';

VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

VueMarkdownEditor.use(vuepressTheme, {
  Prism,
});

const app = createApp(App)
axios.defaults.baseURL = 'http://127.0.0.1:8000/';

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate);
app.use(mavonEditor).use(VMdPreview).use(VueMarkdownEditor);
app.use(pinia).use(router).use(ElementPlus, {locale}).mount('#app')
