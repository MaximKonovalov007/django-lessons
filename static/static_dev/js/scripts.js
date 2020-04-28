$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);

    function basket_updating(product_id, nmb ,is_delete) {
        let data = {};
        data.product_id = product_id;
        data.nmb = nmb;

        let csrf_token =  $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        if(is_delete){
            data["is_delete"] = true;
        }

        let url = form.attr("action");

        console.log(data);

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log('OK');
                console.log(data.product_total_nmb);
                if (data.product_total_nmb || data.product_total_nmb == 0){
                    $("#basket_total_nmb").text("(" + data.product_total_nmb + ")");
                    console.log(data.products);
                    $('.basket-items ul').html("");
                    $.each(data.products, function (key, value) {
                        $('.basket-items ul').append('<li>' + value.name + ' ' + value.nmb + ' шт ' + ' по ' + value.price_per_item + 'RUB за шт. <span class="delete-item">x</span></li>');
                    });
                }
            },
            error: function () {
                console.log("Error!");
            }
        });
    }

    form.on('submit', function(e){
        e.preventDefault();
        let nmb = $('#number').val();
        console.log(nmb);
        let submit_btn = $('#submit_btn');
        let product_id = submit_btn.data('product_id');
        let product_name = submit_btn.data('name');
        let product_price = submit_btn.data('price');
        console.log(product_id);
        console.log(product_name);

        basket_updating(product_id, nmb ,is_delete=false)
    });



    function showing_basket(){
        $('.basket-items').toggleClass('hidden');
    }

    $('.basket-container').mouseover(function (e){
        e.preventDefault();
        showing_basket();
    });

    $('.basket-container').mouseout(function (e){
        e.preventDefault();
        showing_basket();
    });


    $(document).on('click','.delete-item', function (e){
        e.preventDefault();
        let product_id = $(this).data("product_id");
        let nmb = 0;
        basket_updating(product_id, nmb, is_delete=true);
    });

    function calculation_basket_total_amount() {
        let total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function () {
            total_order_amount += parseInt($(this).text());
        });
        $('#total_order_amount').text(total_order_amount);
    }

    calculation_basket_total_amount();

    $(document).on('change', ".product-in-basket-nmb", function () {
        let current_nmb = $(this).val();
        console.log(current_nmb);
        let current_tr = $(this).closest('tr');
        console.log(current_tr);
        let current_price = parseFloat(current_tr.find('.product-price').text());
        let total_amount = current_nmb * current_price;

        current_tr.find('.total-product-in-basket-amount').text(total_amount);

        calculation_basket_total_amount();
    });
});
