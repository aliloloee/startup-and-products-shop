function showAlert (msg, colorClass) {
    clearAlert();
    const div = document.createElement('div');
    div.className = colorClass + ' alert text-center';
    div.appendChild(document.createTextNode(msg));
    const conatiner = document.querySelector('.main-body');
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