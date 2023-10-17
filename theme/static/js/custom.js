

$(function() {
    $('#increment-btn').on("click",function(e) {
        e.preventDefault();

        var inputElement = $('input[name="quantity"]');
        var currentValue = parseInt(inputElement.val());

        if (!isNaN(currentValue) && currentValue < 10) {
            inputElement.val(currentValue + 1);
        }
    });

    $('#decrement-btn').on("click",function(e) {
        e.preventDefault();

        var inputElement = $('input[name="quantity"]');
        var currentValue = parseInt(inputElement.val());

        if (!isNaN(currentValue) && currentValue > 1) {
            inputElement.val(currentValue - 1);
        } 
    });
});
