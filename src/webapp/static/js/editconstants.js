$('.CriticalCount').hide();

$('#replaceParam').change(function () {
    $('.recordLimit').hide();
    $('.CriticalCount').hide();
    
    var value = this.value;
    $('.' + this.value).show();
});