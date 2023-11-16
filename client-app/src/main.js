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

axios.defaults.timeout = 10000;

const app = createApp(App)
axios.defaults.baseURL = 'http://127.0.0.1:8000/';

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate);
app.use(mavonEditor)
app.use(pinia).use(router).use(ElementPlus, {locale}).mount('#app')
