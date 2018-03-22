$(document).ready(function () {
    $('.thumbnail').hover(function () {
        $(this).animate({paddingLeft: '+=0px'}, 200);

    }, function () {
        $(this).animate({paddingLeft: '-=0px'}, 200);
    });
});

