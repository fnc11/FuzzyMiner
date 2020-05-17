import request from '@/utils/request'

export function nodeFilter(data) {
    return request({
        url: 'node_filter',
        method: 'post',
        data: data
    });
}

export function edgeFilter(data) {
    return request({
        url: 'edge_filter',
        method: 'post',
        data: data
    });
}

export function scRatio(data) {
    return request({
        url: 'sc_ratio',
        method: 'data',
        data: data
    });
}

export function cutoff(data) {
    return request({
        url: 'cutoff',
        method: 'data',
        data: data
    });
}

export function preserve(data) {
    return request({
        url: 'preserve',
        method: 'post',
        data: data
    });
}

export function balance(data) {
    return request({
        url: 'balance',
        method: 'post',
        data: data
    });
}

export function metrics(data) {
    return request({
        url: 'metrics',
        method: 'post',
        data: data
    });
}
