

quantity_numbers.forEach(qty => {
    qty.addEventListener('change', e => {
        const product = e.target.parentElement.parentElement;
        console.log(product)
        let data, productid, productqty, features, featureids=[], options, optionids=[];
        productid = e.target.dataset.index;
        productqty = e.target.value;

        features = product.querySelectorAll('.product-feature');
        features.forEach(feature => {
            featureids.push(feature.dataset.index);
        })

        options = product.querySelectorAll('.product-option');
        options.forEach(option => {
            optionids.push(option.dataset.index);
        })

        if (productqty === '0') {
            data = {
            'productid' : productid,
            'featureids' : featureids,
            'optionids' : optionids,
            }
            http.delete(deleteURL, csrfToken, data, function(err, res) {
                if (!err){
                    const response = JSON.parse(res);
                    product.remove();
                    document.getElementById("basket-qty").innerHTML = response.qty;
                    document.getElementById("subtotal").innerHTML = `${numWithCommas(response.subtotal)} Toman`;
                } else {
                    console.log(err);
                }
            })
            return;
        }

        data = {
            'productid' : productid,
            'featureids' : featureids,
            'optionids' : optionids,
            'productqty' : productqty,
        }

        http.put(putURL, csrfToken, data, function(err, res) {
            if (!err){
                const response = JSON.parse(res);
                document.getElementById("basket-qty").innerHTML = response.qty;
                document.getElementById("subtotal").innerHTML = `${numWithCommas(response.subtotal)} Toman`;
            } else {
                console.log(err);
            }
        })
    })
})


products.forEach(product => {
    product.addEventListener('click', e => {
        let productid, features, featureids=[], options, optionids=[], data;

        productid = product.dataset.index;

        features = product.querySelectorAll('.product-feature');
        features.forEach(feature => {
            featureids.push(feature.dataset.index);
        })

        options = product.querySelectorAll('.product-option');
        options.forEach(option => {
            optionids.push(option.dataset.index);
        })

        data = {
            'productid' : productid,
            'featureids' : featureids,
            'optionids' : optionids,
        }

        if (e.target.id === 'delete-button') {
            e.preventDefault();
            http.delete(deleteURL, csrfToken, data, function(err, res) {
                if(!err) {
                    const response = JSON.parse(res);
                    product.remove();
                    document.getElementById("basket-qty").innerHTML = response.qty;
                    document.getElementById("subtotal").innerHTML = `${numWithCommas(response.subtotal)} Toman`;
                } else {
                    console.log(err);
                }
            })
        }
    })
})

function numWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
