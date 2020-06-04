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
            component: () => import('@/components/Help'),
            children: [{
                path: 'windows',
                name: 'Windows',
                component: () => import('@/components/help/guide/Windows')
            }, {
                path: 'mac',
                name: 'Mac',
                component: () => import('@/components/help/guide/Mac')
            }, {
                path: 'linux',
                name: 'Linux',
                component: () => import('@/components/help/guide/Linux')
            }, {
                path: 'pycharm',
                name: 'Pycharm',
                component: () => import('@/components/help/guide/Pycharm')
            }, {
                path: 'generate',
                name: 'Generate',
                component: () => import('@/components/help/use/Generate')
            }, {
                path: 'node',
                name: 'NodeFilter',
                component: () => import('@/components/help/use/NodeFilter')
            }, {
                path: 'edge',
                name: 'EdgeFilter',
                component: () => import('@/components/help/use/EdgeFilter')
            }, {
                path: 'concurrency',
                name: 'ConcurrencyFilter',
                component: () => import('@/components/help/use/ConcurrencyFilter')
            }, {
                path: 'unary',
                name: 'UnarySignificance',
                component: () => import('@/components/help/use/UnarySignificance')
            }, {
                path: 'binary',
                name: 'BinarySignificance',
                component: () => import('@/components/help/use/BinarySignificance')
            }, {
                path: 'correlation',
                name: 'BinaryCorrelation',
                component: () => import('@/components/help/use/BinaryCorrelation')
            }, {
                path: 'linear',
                name: 'LinearAttenuation',
                component: () => import('@/components/help/use/LinearAttenuation')
            }, {
                path: 'nroot',
                name: 'NRootAttenuation',
                component: () => import('@/components/help/use/NRootAttenuation')
            }, {
                path: 'snapshot',
                name: 'SnapShot',
                component: () => import('@/components/help/use/SnapShot')
            }, {
                path: 'video',
                name: 'Video',
                component: () => import('@/components/help/Video')
            }, {
                path: 'faqs',
                name: 'Faqs',
                component: () => import('@/components/help/Faqs')
            }]
        }
    ]
})
