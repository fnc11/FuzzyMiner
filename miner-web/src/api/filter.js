import request from '@/utils/request'

export function nodeFilter() {
    return request({
        url: 'node_filter',
        method: 'get'
    });
}

export function scRatio() {
    return request({
        url: 'sc_ratio',
        method: 'get'
    });
}

export function cutoff() {
    return request({
        url: 'cutoff',
        method: 'get'
    });
}

export function preserve() {
    return request({
        url: 'preserve',
        method: 'get'
    });
}

export function balance() {
    return request({
        url: 'balance',
        method: 'get'
    });
}

export function metrics() {
    return request({
        url: 'metrics',
        method: 'get'
    });
}
