!(function ($) {
  "use strict";
  $(document).on('click', '.mobile-nav-toggle', function (e) {
    $('body').toggleClass('mobile-nav-active');
    $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu ');
  });

  $(document).click(function (e) {
    var container = $(".mobile-nav-toggle");
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      if ($('body').hasClass('mobile-nav-active')) {
        $('body').removeClass('mobile-nav-active');
        $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu ');
      }
    }
  });

  $(document).on('click', '.one', function (e) {
    if ($('.one').hasClass('d-none')) {
      $('.sub1').toggleClass('d-none');
    }
    else {
      $('.sub1').toggleClass('d-none');
    }
  });
  $(document).on('click', '.two', function (e) {
    if ($('.two').hasClass('d-none')) {
      $('.sub2').toggleClass('d-none');
    }
    else {
      $('.sub2').toggleClass('d-none');
    }
  });
  $(document).on('click', '.three', function (e) {
    if ($('.three').hasClass('d-none')) {
      $('.sub3').toggleClass('d-none');
    }
    else {
      $('.sub3').toggleClass('d-none');
    }
  });
  $(document).on('click', '.four', function (e) {
    if ($('.four').hasClass('d-none')) {
      $('.sub4').toggleClass('d-none');
    }
    else {
      $('.sub4').toggleClass('d-none');
    }
  });
})(jQuery);


