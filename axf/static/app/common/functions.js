function addCart(goods_id) {
   // $.get('/app/addCart/?goods_id=' + goods_id, function (msg) {
   //     if(msg.code == 200){
   //         $('#num_' + goods_id).text(msg.c_num)
   //     }else{
   //        alter(msg.msg)
   //     }
   // });
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/app/addCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {

            if(msg.code == 200){
                count_price();
                $('#num_' + goods_id).text(msg.c_num)
            }else{
                alter(msg.msg);
            }
        },
        error: function () {
            alert('请求失败')
        }
    });
}


function subCart(goods_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: '/app/subCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},

        success: function (data) {

            if(data.code == 200){
                count_price();
                $('#num_' + goods_id).text(data.c_num)
            }
        },
        error: function () {
            alert('请求失败')
        }
    });
}


function changeSelectStatus(cart_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: '/app/changeSelectStatus/',
        type: 'POST',
        data: {'cart_id': cart_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {

            if(data.code == 200){
                count_price();
                if(data.is_select){
                    $('#cart_id_' + cart_id).text('√')
                }else{
                    $('#cart_id_' + cart_id).text('×')
                }
            }
        },
        error: function () {
            alert('请求失败');
        }

    });
}


function change_order(order_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/app/changeOrderStatus/',
        type: 'POST',
        data: {'order_id': order_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {

            if (msg.code == 200){
                location.href = '/app/mine/'
            }
        },
        error: function (msg) {
            alert('订单状态修改失败')
        }
    });
}

function all_select(i) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/app/allSelect/',
        type: 'POST',
        data: {'all_select': i},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {

            if(msg.code == 200){
                count_price();

                for(var a=0; a<msg.ids.length; a++){

                    if(msg.flag){

                        s = '<span id="cart_id_' + msg.ids[a] + '" onclick="changeSelectStatus(' + msg.ids[a] + ')">√</span>';
                        $('#changeselect_' + msg.ids[a]).html(s);

                        $('#all_select_id').attr({'onclick': 'all_select(1)'});
                        $('#select_id').html('√')
                    }else{

                        s = '<span id="cart_id_' + msg.ids[a] + '" onclick="changeSelectStatus(' + msg.ids[a] + ')">×</span>';
                        $('#changeselect_' + msg.ids[a]).html(s);


                        $('#all_select_id').attr({'onclick': 'all_select(0)'});
                        $('#select_id').html('×')
                    }
                }
            }
        },
        error: function (msg) {
            alert('请求失败')
        }
    });
}

// 默认情况下的显示效果
$.get('/app/count_price/', function (msg) {
    if(msg.code == '200'){
        $('#count_price').html('总价:' + msg.count_price)
    }
})

// 点击全选等按钮后的显示效果
function count_price() {
    $.get('/app/count_price/', function (msg) {
        if(msg.code == '200'){
            $('#count_price').html('总价:' + msg.count_price)
        }
    })
}
