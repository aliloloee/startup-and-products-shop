let option_values = {};
    
document.addEventListener('DOMContentLoaded', e => {
    let option_numbers = options.length;
    var i;
    for (i=0; i<option_numbers; i++) {
        option_values[`option-${i + 1}`] = null;
    }
})

addToBasketBtn.addEventListener('click', e => {
    e.preventDefault();
    let data;
    const productid = e.target.value;
    let featureids = [];
    let optionids = [];
    const productqty = qty.value;

    if (productqty === '0' ) return;

    features.forEach(feature => {
        if (feature.checked){
            featureids.push(feature.dataset.index);
        }
    })

    options.forEach(option => {
        if (option.value !== 'None'){
            optionids.push(option.value);
        }
    })

    data = {
        'productid' : productid,
        'featureids' : featureids,
        'optionids' : optionids,
        'productqty' : productqty,
    }

    http.post(postURL, csrfToken, data, function(err, res) {
        if (!err){
            response = JSON.parse(res);
            document.getElementById("basket-qty").innerHTML = response.qty;
            showAlert('Product added to cart successfully', 'alert-success');
        } else {
            console.log(err);
        }
    })
})

options.forEach(option => {
    option.addEventListener('change', e => {
        e.preventDefault();

        let option_frontend_id;
        option_frontend_id = option.id;

        if (option.value !== 'None') {
            let option_backend_id, url;
            option_backend_id = option.value;
            // url = getOptionURL.replace('0', option_backend_id);

            // http.get(url, function(err, res) {
            //     if (!err){
            //         const response = JSON.parse(res);
            //         let currentPrice = parseFloat(productPrice.innerText.substring(1));
            //         if (option_values[option_frontend_id]) {
            //             let last_item_price = option_values[option_frontend_id][1];
            //             productPrice.innerText = `£${roundNumber(currentPrice + parseFloat(response.price) - parseFloat(last_item_price), 2)}`;
            //         } else {
            //             productPrice.innerText = `£${roundNumber(currentPrice + parseFloat(response.price), 2)}`;
            //         }
            //         option_values[option_frontend_id] = [option_backend_id, response.price];
            //     } else {
            //         console.log(err);
            //     }
            // })

            const response = option.options[option.selectedIndex].dataset.price;
            let currentPrice = parseFloat(productPrice.innerText.split(" ")[0].split(",").join(""));
            if (option_values[option_frontend_id]) {
                let last_item_price = option_values[option_frontend_id][1];
                productPrice.innerText = `${ numWithCommas(currentPrice + parseFloat(response) - parseFloat(last_item_price)) } toman`;

            } else {
                productPrice.innerText = `${ numWithCommas(currentPrice + parseFloat(response)) } toman`;

            }
            option_values[option_frontend_id] = [option_backend_id, response];

        } else {
            let currentPrice = parseFloat(productPrice.innerText.split(" ")[0].split(",").join(""));
            if (option_values[option_frontend_id]) {
                let last_item_price = option_values[option_frontend_id][1];
                productPrice.innerText = `${ numWithCommas(currentPrice - parseFloat(last_item_price)) } toman`;
            }
            option_values[option_frontend_id] = null;
        }
    })
})


features.forEach(feature => {
    feature.addEventListener('change', e => {
        // let i, url;
        // i = e.target.dataset.index;
        // url = getFeatureURL.replace('0', i);

        // http.get(url, function(err, res) {
        //     if (!err){
        //         const response = JSON.parse(res);
        //         let currentPrice = parseFloat(productPrice.innerText.substring(1));
        //         if (e.target.checked){
        //             productPrice.innerText = `£${roundNumber(currentPrice + parseFloat(response.price), 2)}`;
        //         } else {
        //             productPrice.innerText = `£${roundNumber(currentPrice - parseFloat(response.price), 2)}`;
        //         }
        //     } else {
        //         console.log(err);
        //     }
        // })

        let feature_price = e.target.dataset.price;
        let currentPrice = parseFloat(productPrice.innerText.split(" ")[0].split(",").join(""));

        if (e.target.checked){
            productPrice.innerText = `${ numWithCommas(currentPrice + parseFloat(feature_price)) } toman`;
        } else {
            productPrice.innerText = `${ numWithCommas(currentPrice - parseFloat(feature_price)) } toman`;
        }


    })
})


function numWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


function showAlert (msg, colorClass) {
    clearAlert();
    const div = document.createElement('div');
    div.className = colorClass + ' alert text-center';
    div.appendChild(document.createTextNode(msg));
    const conatiner = document.querySelector('.product');
    conatiner.parentNode.insertBefore(div, conatiner);
    setTimeout(() => {
        clearAlert();
    }, 3000);
}

function clearAlert(){
    const currentAlert = document.querySelector('.alert');
    if (currentAlert){
        currentAlert.remove();
    };
}
