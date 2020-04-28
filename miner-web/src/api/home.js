import request from '@/utils/request';

export function upload(form) {
    return request({
        url: '/upload',
        method: 'post',
        data: form,
        header: {
            'Content-Type': 'multipart/form-data'
        }
    });
}
