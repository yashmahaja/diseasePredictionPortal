$('#right-arrow').click(function(){
    var currentSlide = $('.innerbox.active');
    var nextSlide = currentSlide.next();

    currentSlide.fadeOut(300).removeClass('active');
    nextSlide.fadeIn(300).addClass('active');

    if(nextSlide.length == 0){
        $('.innerbox').first().fadeIn(300).addClass('active');
    }
});

$('#left-arrow').click(function(){
    var currentSlide = $('.innerbox.active');
    var prevSlide = currentSlide.prev();
    currentSlide.fadeOut(300).removeClass('active');
    prevSlide.fadeIn(300).addClass('active');

    if(prevSlide.length == 0){
        $('.innerbox').last().fadeIn(300).addClass('active');
    }
});