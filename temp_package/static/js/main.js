// 全局JavaScript函数

// 初始化工具提示
$(function () {
    $('[data-bs-toggle="tooltip"]').tooltip()
});

// 初始化弹出框
$(function () {
    $('[data-bs-toggle="popover"]').popover()
});

// 页面加载动画
$(window).on('load', function() {
    $('.loading-overlay').fadeOut();
});

// 全局AJAX错误处理
$(document).ajaxError(function(event, xhr) {
    if (xhr.status === 403) {
        alert('您没有权限执行此操作');
    } else if (xhr.status === 401) {
        window.location.href = '/login/?next=' + window.location.pathname;
    }
});

// 全局日期选择器初始化
$('.datepicker').datepicker({
    format: 'yyyy-mm-dd',
    autoclose: true,
    todayHighlight: true
});