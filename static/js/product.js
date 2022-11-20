//Number of Quantity user wants

var increase = document.getElementById('increaseQuantity');
var decrease = document.getElementById('decreaseQuantity');
var num = document.getElementById('num');

//increases the value
var data = JSON.parse(document.getElementById('details').textContent);
var quantity = data['quantity']
increase.addEventListener("click", function() {   
    console.log('Increase Invoke');   
    //console.log('value : ',data['quantity']);
    if (num.textContent < quantity){
        console.log(num.textContent<quantity)
        num.textContent = Number(num.textContent) + 1
        console.log('Product Number:',num.textContent)
    
    }
    
})

//decreases the value
decrease.addEventListener("click", function() {
    console.log('Decrease Invoke');
    console.log(num.textContent);
    if (num.textContent == Number(0)) {
        num.textContent = 0;
    } else {
        num.textContent = Number(num.textContent) - 1
    }
})

// ProductData to Django
function product_size(){
    /*
    var small  = document.getElementById('small').textContent
    var medium = document.getElementById('medium').textContent
    var large = document.getElementById('large').textContent
    

    var productSize = document.getElementById(id).textContent
    */
    var productName = document.getElementById('productname').textContent
    var productprice = document.getElementById('productprice').textContent
    var productReview = document.getElementById('productreviews').textContent
    
    var data = {"productName":productName
    ,"productprice":productprice,"productReview":productReview}
    console.log(data)
    return data

}

