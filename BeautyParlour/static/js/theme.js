(function ($) {

    "use strict";

    var navbar = $('.header-menu, .middle_menu_area, .header_white_menu');

    var nav_offset_top = $('.header-menu, .middle_menu_area, .header_white_menu').offset().top + 60;

    /*-------------------------------------------------------------------------------

      Navbar 

    -------------------------------------------------------------------------------*/

    //    navbar.affix({
    //
    //      offset: {
    //
    //        top: nav_offset_top,
    //
    //      }
    //
    //    });


    navbar.on('affix.bs.affix', function () {

        if (!navbar.hasClass('affix')) {

            navbar.addClass('animated slideInDown');
        }

    });

    navbar.on('affixed-top.bs.affix', function () {

        navbar.removeClass('animated slideInDown');

    });

    /*------- search form js -------*/

    $('.search-dropdown a').on('click', function () {
        $(".header-search").slideToggle();
        // if( $(this).parent().hasClass('open-search') ){

        //     $(this).parent().removeClass('open-search')

        // }

        // else{

        //     $(this).parent().addClass('open-search')

        //     $('.offcanvas_closer').addClass('show')

        // }

        return false

    });

    //navigation-header-js-Start


    /*------- search form js -------*/

    $('.serach_icon').on('click', function () {
        $(".search-wrap, .search-overlay").fadeIn();
        return false

    });

    $('.serach-close').on('click', function () {
        $(".search-wrap").fadeOut();
        return false

    });

    //navigation-header-js-Start


    $(document).ready(function () {
        $(' .navbar-nav > li > .dropdown-menu > li').on('click', function () {

            if ($(this).parent().parent().hasClass('open')) {

                $(this).find(".dropdown-menu").toggleClass("opensubmenu");

                if ($(this).children().hasClass("dropdown-menu")) {

                    //                            return false;

                    event.stopPropagation();

                }

            }

        });


        $(' .header-part .navbar-inverse .navbar-nav > li ').on('click', function () {

            //                                 if($(this).hasClass('dropdown-toggle')){

            $(".dropdown-menu").removeClass("opensubmenu");
            //                                    }

        });


        if ($(window).width() < 991) {

            $('.megamenu-content .title ').on('click', function () {

                $(".megamenu-content .title").not($(this)).siblings().hide();

                $(this).siblings().toggle();

                //                        return false;

                event.stopPropagation();

            });

        }

    });

    //navigation-header-js-End    


    /* Main Slide Function*/

    function sliderCarosule() {

        if ($('.slider_area .owl-carousel').length) {

            $('.slider_area .owl-carousel').owlCarousel({

                loop: true,

                nav: true,

                dots: true,

                autoplay: true,

                singleItem: true,

                // animateIn: 'fadeIn',

                // animateOut: 'fadeOut',<i class="fa-light fa-arrow-left-long"></i>

                navText: [

                    '<i class="fa fa-angle-left"></i>',

                    '<i class="fa fa-angle-right"></i>'

                ],

                smartSpeed: 1500,

                autoplayHoverPause: true,

                responsive: {

                    0: {

                        items: 1

                    },

                    480: {

                        items: 1

                    },

                    600: {

                        items: 1

                    },

                    1000: {

                        items: 1

                    },

                    1200: {

                        items: 1

                    },

                    1920: {

                        items: 1

                    }

                }

            });

        }

    }

    sliderCarosule();

 
    /* Service Slider Function*/

/* Clients Logo Function*/

function ourworkCarosule () {

    if ($('#ourwork .owl-carousel').length) {

        $('#ourwork .owl-carousel').owlCarousel({

            loop: true,

            nav: true,

            dots: false,

            margin:0,

            autoWidth: true,

            navText: [

                '<i class="fa fa-arrow-left"></i>',

                '<i class="fa fa-arrow-right"></i>',

            ],

            autoplay: true,

            smartSpeed: 1500,

            autoplayTimeout: 3000,

            autoplayHoverPause: true,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                600:{

                    items:1

                },

                1000:{

                    items:2

                },

                1200:{

                    items:1

                }

            }

        });

    }

}

ourworkCarosule();


    function aboutus() {

        if ($('.whoweare-slider.owl-carousel').length) {

            $('.whoweare-slider.owl-carousel').owlCarousel({

                loop: false,

                margin: 30,

                nav: false,

                dots: true,

                singleItem: true,
                // animateIn: 'fadeIn',
                // animateOut: 'fadeOut',

                // navText: [

                //     '<i class="fa fa-angle-left"></i>',

                //     '<i class="fa fa-angle-right"></i>'

                // ],

                smartSpeed: 1000,

                autoplayHoverPause: true,

                responsive: {

                    0: {

                        items: 1

                    },

                }

            });

        }

    }

    aboutus();

    /* Service Slider Function Start*/

function serviceCarosule () {

    if ($('.service-section .owl-carousel').length) {

        $('.service-section .owl-carousel').owlCarousel({

            loop: true,

            margin: 20,

            nav: true,

            dots: false,

            autoplay: true,

            navText: [

                '<i class="fa fa-arrow-left"></i>',

                '<i class="fa fa-arrow-right"></i>',

            ],

            smartSpeed: 1500,

            autoplayHoverPause: true,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                600:{

                    items:2

                },

                1000:{

                    items:3

                },

                1200:{

                    items:3

                },

                1920:{

                    items:3

                }

            }

        });

    }

}

serviceCarosule();

function service2Carosule() {

    if ($('.service2 .owl-carousel').length) {

        $('.service2 .owl-carousel').owlCarousel({

            loop: true,
            margin: 15,

            nav: true,

            dots: false,

            autoplay: true,
            autoheight:true,
            singleItem: true,
            center:true,

/*            animateIn: 'fadeIn',

            animateOut: 'fadeOut',*/



                navText: [

                    '<i class="fa fa-angle-left"></i>',

                    '<i class="fa fa-angle-right"></i>'

                ],
                responsiveClass: true,

                smartSpeed: 1500,

                autoplayHoverPause: true,

                responsive: {

                    0: {

                        items: 1

                    },

                    480: {

                        items: 1

                    },

                    600: {

                        items: 2

                    },

                    1000: {

                        items: 3

                    },

                    1200: {

                        items: 3

                    },

                    1920: {

                        items: 3

                    }

                }

            });

        }

    }

 service2Carosule();



function testimonialareaCarosule () {

    if ($('.testimonial-area .owl-carousel').length) {

        $('.testimonial-area .owl-carousel').owlCarousel({

            loop: true,

            margin: 30,

            nav: false,

            dots: true,

            autoplay: true,

            navText: [

                '<i class="fa fa-arrow-left"></i>',

                    '<i class="fa fa-arrow-right"></i>',

            ],

            smartSpeed: 1500,

            autoplayHoverPause: true,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                600:{

                    items:1

                },

                1000:{

                    items:1

                },

                1200:{

                    items:1

                },

                1920:{

                    items:1

                }

            }

        });

    }

}

testimonialareaCarosule ();


function galleryCarosule() {

    if ($('.gallery .owl-carousel').length) {

        $('.gallery .owl-carousel').owlCarousel({

            loop: true,
            margin: 15,

            nav: false,

            dots: false,

            autoplay: true,
            autoheight:true,
            singleItem: true,
            center:true,

/*            animateIn: 'fadeIn',

            animateOut: 'fadeOut',*/



                navText: [

                    '<i class="fa fa-angle-left"></i>',

                    '<i class="fa fa-angle-right"></i>'

                ],
                responsiveClass: true,

                smartSpeed: 1500,

                autoplayHoverPause: true,

                responsive: {

                    0: {

                        items: 1

                    },

                    480: {

                        items: 1

                    },

                    600: {

                        items: 2

                    },

                    1000: {

                        items: 3

                    },

                    1200: {

                        items: 3

                    },

                    1920: {

                        items: 3

                    }

                }

            });

        }

    }

 galleryCarosule();



/* Clients Logo Function*/

function clientCarosule () {

    if ($('#clients .owl-carousel').length) {

        $('#clients .owl-carousel').owlCarousel({

            loop: true,

            nav: true,

            dots: false,

            margin:10,

            autoWidth: true,

            navText: [

                '<i class="fa fa-arrow-left"></i>',

                '<i class="fa fa-arrow-right"></i>',

            ],

            autoplay: true,

            smartSpeed: 1500,

            autoplayTimeout: 3000,

            autoplayHoverPause: true,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:2

                },

                600:{

                    items:3

                },

                1000:{

                    items:5

                },

                1200:{

                    items:7

                }

            }

        });

    }

}

clientCarosule();



    /* portfolio Function Start*/

    function portfolio() {

        if ($('.portfolio-residentslider.owl-carousel, .portfolio-commercialslider.owl-carousel').length) {

            $('.portfolio-residentslider.owl-carousel, .portfolio-commercialslider.owl-carousel').owlCarousel({
                loop: true,
                margin: 5,
                nav: true,
                items: 1,
                dots: true,
                //                animateIn: 'fadeIn',
                //                animateOut: 'fadeOut',
                autoplay: false,
                navText: [

                    '<span class="fa fa-arrow-left"></span>',

                    '<span class="fa fa-arrow-right"></span>',

                ],

                autoplayHoverPause: true,


            });

        }

    }

    portfolio();



    /* portfolio Function End*/

 


    /* Counter Function*/

    function CounterNumberChanger() {
        var timer = $('.timer');

        if (timer.length) {

            timer.appear(function () {
                

                timer.countTo();

            })

        }

    }

    CounterNumberChanger();


    /* Contact Form Function*/

    function contactFormValidation() {

        if ($('.contact_us_form').length) {

            $('.contact_us_form').validate({ // initialize the plugin

                rules: {

                    name: {

                        required: true

                    },

                    email: {

                        required: true,

                        email: true

                    },

                    message: {

                        required: true

                    },

                    subject: {

                        required: true

                    }

                },

                submitHandler: function (form) {

                    // sending value with ajax request

                    $.post($(form).attr('action'), $(form).serialize(), function (response) {

                        $(form).parent('div').append(response);

                        $(form).find('input[type="text"]').val('');

                        $(form).find('input[type="email"]').val('');

                        $(form).find('textarea').val('');

                    });

                    return false;

                }

            });

        }

    }

    //contactFormValidation ();   


    /* Video Popup Function*/

    $(document).ready(function () {

        $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({

            disableOn: 700,

            type: 'iframe',

            mainClass: 'mfp-fade',

            removalDelay: 160,

            preloader: false,

            fixedContentPos: false

        });

    });


    // scroll bottom to top button js Start

    $(document).ready(function () {

        $(window).scroll(function () {

            if ($(this).scrollTop() > 150) {

                $('#scroll').fadeIn();

            } else {

                $('#scroll').fadeOut();

            }

        });

        $('#scroll').on('click', function () {

            $("html, body").animate({ scrollTop: 0 }, 600);

            return false;

        });

    });



    //  scroll bottom to top button js End

    // === Count animations --start-- ===

    function Utils() {
    }
    Utils.prototype = {
        constructor: Utils,
        isElementInView: function (element, fullyInView) {
            if ($('.project-experience .count').hasClass('count')) {
                var pageTop = $(window).scrollTop();
                var pageBottom = pageTop + $(window).height();

                var elementTop = $(element).offset().top;

                var elementBottom = elementTop + $(element).height();

                if (fullyInView === true) {
                    return ((pageTop < elementTop) && (pageBottom > elementBottom));
                } else {
                    return ((elementTop <= pageBottom) && (elementBottom >= pageTop));
                }
            }
        }
    };
    var Utils = new Utils();

    // ===**=== // 

    var count = 0;
    $(window).on('resize scroll', function () {
        var isElementInView = Utils.isElementInView($('.count'), true);
        if (isElementInView && !count) {
            $('.count').each(function () {
                $(this).prop('Counter', 0).animate({
                    Counter: $(this).text()
                }, {
                    duration: 1000,
                    easing: 'swing',
                    step: function (now) {
                        $(this).text(Math.ceil(now));
                    }
                });
            });
            count++;
        }
    });
    // === Count animations --end-- ===   


})(jQuery);


//             .........WOW animation js Start.........
jQuery(document).ready(function () {
    //===================
    //  WOW
    //  do not touch
    //===================
    new WOW().init();
});
//             .........WOW animation js End.........


//fixed header on scroll js Start
$(window).scroll(function () {
    if ($(window).scrollTop() >= 160) {
        $('.main-header').addClass('scroll-header animated slideInDown');
    } else {
        $('.main-header').removeClass('scroll-header animated slideInDown');
    }
});
    //fixed header on scroll js End