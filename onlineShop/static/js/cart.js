
function updateUserCart(productId, action) {
    const url = '/update-cart/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({productId, action})
    })
        .then(response => response.json())
        .then(data => console.log(data))
}



document.querySelectorAll('.cart-change').forEach(function (button) {
    button.addEventListener('click', function () {
        const productId = this.dataset.product
        const action = this.dataset.action
        console.log(productId, action)
        if (user === 'AnonymousUser') {
            console.log('You are not logged in..')
        } else {
            updateUserCart(productId, action)
        }
    })
})