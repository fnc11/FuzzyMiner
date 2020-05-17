import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Home',
            component: () => import('@/components/Home')
        },
        {
            path: '/filter',
            name: 'Filter',
            component: () => import('@/components/Filter')
        },
        {
            path: '/help',
            name: 'Help',
            component: () => import('@/components/Help')
        }
    ]
})
