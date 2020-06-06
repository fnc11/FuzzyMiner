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

export function concurrencyFilter(data) {
    return request({
        url: 'concurrency_filter',
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
