import Vue from 'vue';
import router from './router';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import store from './store';
import Viewer from "v-viewer";
import 'viewerjs/dist/viewer.css';

Vue.use(Viewer, {name: 'viewer'});
Vue.use(ElementUI);

Vue.config.productionTip = false;

Viewer.setDefaults({
    'inline': true,
    'button': true,
    "navbar": true,
    "title": true,
    "toolbar": true,
    "tooltip": true,
    "movable": true,
    "zoomable": true,
    "rotatable": true,
    "scalable": true,
    "transition": true,
    "fullscreen": true,
    "keyboard": true,
    "backdrop": true,
    "url": "data-source"
});

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app');
