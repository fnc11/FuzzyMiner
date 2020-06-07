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
            redirect: '/help/home',
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
                path: 'attenuation',
                name: 'Attenuation',
                component: () => import('@/components/help/use/Attenuation')
            }, {
                path: 'nroot',
                name: 'NRootAttenuation',
                component: () => import('@/components/help/use/NRootAttenuation')
            }, {
                path: 'example',
                name: 'Example',
                component: () => import('@/components/help/use/Example')
            }, {
                path: 'video',
                name: 'Video',
                component: () => import('@/components/help/Video')
            }, {
                path: 'faqs',
                name: 'Faqs',
                component: () => import('@/components/help/Faqs')
            }, {
                path:'graph',
                name:'Graph',
                component:() => import('@/components/help/use/Graph')
            }, {
                path:'home',
                name:'Homescreen',
                component:() => import('@/components/help/use/Homescreen')
            }, {
                path:'filter',
                name:'Filterscreen',
                component:() => import('@/components/help/use/Filterscreen')
            }, {
                path:'metrics',
                name:'Metrics',
                component:() => import('@/components/help/use/Metrics')
            }, {
                path:'helpscreen',
                name:'Helpscreen',
                component:() => import('@/components/help/use/Helpscreen')
            }]
        },

    ]
})
