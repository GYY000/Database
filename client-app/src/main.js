import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from "axios";
import store from "@/store";
import locale from 'element-plus/es/locale/lang/zh-cn'
import {ElementPlus} from "@element-plus/icons-vue";

axios.defaults.timeout = 2000;

const app = createApp(App)
axios.defaults.baseURL = 'http://127.0.0.1:8000/';

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(store).use(router).use(ElementPlus).use(ElementPlus, {locale}).mount('#app')
