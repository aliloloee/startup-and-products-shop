const delete_buttons = document.getElementsByName('delete-button');
const quantity_numbers = document.getElementsByName('quantity');
const add_btn = document.getElementById('add-button');

delete_buttons.forEach(btn => {
    btn.addEventListener('click', e => {
        e.preventDefault();
        let product_id, product, data;

        product_id = btn.dataset.index;
        product = e.target.parentElement.parentElement.parentElement;

        data = {
            'product_id' : product_id,
        }

        http.delete(change_url, csrfToken, data, function(err, res) {
            if (!err) {
                response = JSON.parse(res);
                console.log(response['info']);
                product.remove();
            } else {
                console.log(err)
            }
        })
    })
})

quantity_numbers.forEach(qty => {
    qty.addEventListener('change', e => {
        e.preventDefault();
        qty.disabled = true;
        let product_id, productqty, data;
        product_id = qty.dataset.index;
        productqty = qty.value;

        if (productqty === '0') {
            product = qty.parentElement.parentElement;

            data = {
            'product_id' : product_id,
            }

            http.delete(change_url, csrfToken, data, function(err, res) {
                if (!err) {
                    response = JSON.parse(res);
                    console.log(response['info']);
                    product.remove();
                } else {
                    console.log(err)
                }
            })
            return;
        }

        data = {
            'productqty' : productqty,
            'product_id' : product_id,
        }

        http.put(change_url, csrfToken, data, function(err, res) {
            if(!err) {
                response = JSON.parse(res);
                console.log(response['item_cost']);
                document.getElementById(`item-cost-${product_id}`).innerText = response['item_cost'];
                qty.disabled = false;
            } else {
                console.log(err);
            }
        })
    })
})

add_btn.addEventListener('click', e => {
    e.preventDefault();
    http.get(change_url, function(err, res) {
        if(!err){
            response = JSON.parse(JSON.parse(res)['serialized_products']);
            console.log(response);
        }else {
            console.log(err);
        }
    })
})