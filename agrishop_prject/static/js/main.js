(function($) {
    'use strict';

    /*=======================================
         PRELOADER                     
    ======================================= */
    $(window).on('load', function() {
        $('#preloader').fadeOut('slow', function() {
            $(this).remove();
        });
        $(".slides__preload_wrapper").fadeOut(1500);
    });

    $('#showlogin, #showcoupon').on('click', function() {
        $(this).parent().next().slideToggle(600);
    }); 
 
    /* =======================================
        For slider
    =======================================*/
    $(".slider_home").owlCarousel({
        items: 1,
        nav: true,
        dots: true,
        autoplay: true,
        autoplayTimeout: 9000, // Default is 5000
        smartSpeed: 1000, // Default is 250
        loop: true,
        navText: ["<i class='icon-glyph-205'></i>", "<i class='icon-glyph-204'></i>"],
        mouseDrag: false,
        touchDrag: false,
    });


    /*=======================================
        slider Section
     ========================================== */
    $(".search_icon").on('click', function() {
            $(".search_icon_inr").slideToggle();
        });
    $(".slider_home").on("translate.owl.carousel", function() {
        $(".single_slider h2, .single_slider h5, .single_slider p").removeClass("animated fadeInUp").css("opacity", "0");
        $(".single_slider .slider_btn").removeClass("animated fadeInDown").css("opacity", "0");
    });

    $(".slider_home").on("translated.owl.carousel", function() {
        $(".single_slider h2, .single_slider h5, .single_slider p").addClass("animated fadeInUp").css("opacity", "1");
        $(".single_slider .slider_btn").addClass("animated fadeInDown").css("opacity", "1");
    });

      /* =======================================
           Testimonial Section 
       =======================================*/
    $("#testimonial").owlCarousel({
        autoPlay: 3000, //Set AutoPlay to 5 seconds
        autoplay: true,
        smartSpeed: 1000, // Default is 250
        items: 1, //Set Testimonial items
        loop: true,
        margin: 30,
        singleItem: true,
        touchDrag: true,
        mouseDrag: true,
        pagination: true,
        nav: true,
        dots: false,
        navText: ["<i class='icon-glyph-41'></i>", "<i class='icon-glyph-40'></i>"],
        responsive: {
            1200: {
                items: 1
            },
            992: {
                items: 1
            },
            768: {
                items: 1
            },
            480: {
                items: 1
            },
            320: {
                items: 1
            },
            280: {
                items: 1
            }
        }
    });

    /*=======================================
        Client Section  
    =======================================*/
    $("#client").owlCarousel({
        autoPlay: 3000, //Set AutoPlay to 5 seconds
        autoplay: true,
        smartSpeed: 2000, // Default is 250
        items: 5,
        loop: true,
        touchDrag: true,
        mouseDrag: true,
        pagination: false,
        dots: false,
        nav: false,
        navText: ["<i class='logo-nav-icon'></i>", "<i class='logo-nav-icon'></i>"],
        responsive: {
            1200: {
                items: 5
            },
            992: {
                items: 5
            },
            768: {
                items: 4
            },
            480: {
                items: 3
            },
            320: {
                items: 2
            },
            280: {
                items: 2
            }
        }
    }); 

    /*=======================================
        Product  slider  
    =======================================*/

    $('.project_list_one').each( function () {
        $('.project_slider_one').slick({
            centerMode: true,
            centerPadding: '200px',
            slidesToShow: 3,
            slidesToScroll: 1,
            arrows: false,
            dots: false,
            autoplay: true,
            autoplaySpeed: 6000,
            prevArrow: '<i class="icon-glyph-204"></i>',
            nextArrow: '<i class="icon-glyph-204"></i>',
            responsive: [
                {
                    breakpoint: 1199,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1,
                        centerMode: true,
                        centerPadding: '80px',
                        arrows: false,
                        dots: false,
                    }
                },
                {
                    breakpoint: 991,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1,
                        centerPadding: '40px',
                        centerMode: false,
                        arrows: false,
                        dots: false
                    }
                },
                {
                    breakpoint: 767,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1, 
                        centerMode: false,
                        arrows: false,
                        dots: false
                    }
                },
                {
                    breakpoint: 580,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        centerMode: false,
                        arrows: false,
                        dots: false
                    }
                }
            ]
        });

         $('.btn-left').click(function(){
          $(this).parents('.project_list_one').find('.project_slider_one').slick('slickPrev');
        });

        $('.btn-right').click(function(){
          $(this).parents('.project_list_one').find('.project_slider_one').slick('slickNext');
        });

    });
 


    /* =======================================
            single Page Nav
     =======================================*/
 
    // The actual plugin
    $('.single-page-nav').singlePageNav({
        offset: $('.single-page-nav').outerHeight(),
        filter: ':not(.external)',
        updateHash: true,
    });

    /* =======================================
        For Menu
    =======================================*/
    $("#navigation").menumaker({
        title: "",
        format: "multitoggle"
    });

    /* =======================================
    		WOW ANIMATION
    ======================================= */
    var wow = new WOW({
        mobile: false
    });
    wow.init();


    /*=======================================
        Scroll Top
    =======================================*/
    $(".scrollup").on('click', function() {
        $('html,body').animate({
            'scrollTop': '0'
        }, 4000);
        return false;
    });

 /*----------------------------
 cart-plus-minus-button
------------------------------ */
    $(".cart-plus-minus").append('<div class="dec qtybutton">-</i></div><div class="inc qtybutton">+</div>');

    $(".qtybutton").on("click", function() {
        var $button = $(this);
        var oldValue = $button.parent().find("input").val();
        if ($button.text() == "+") {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        $button.parent().find("input").val(newVal);
    });

 /*----------------------------
  Shop carousel 
------------------------------ */
    $('.single-thumbnail-big').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.single-thumbnail-small'
    });
    $('.single-thumbnail-small').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        asNavFor: '.single-thumbnail-big',
        dots: false,
        centerMode: true,
        focusOnSelect: true,
        arrows: false,
        prevArrow: '<button type="button" class="custom-prev"><i class="fa fa-long-arrow-left"></i></button>',
        nextArrow: '<button type="button" class="custom-next"><i class="fa fa-long-arrow-right"></i></button>',
            responsive: [
                {
                    breakpoint: 767,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1, 
                        centerMode: false,
                        arrows: false,
                        dots: false
                    }
                },
                {
                    breakpoint: 580,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        centerMode: false,
                        arrows: false,
                        dots: false
                    }
                }
            ]


    }); 
    

/* =======================================
     Client Section  
=======================================*/
  $("#related_prod").owlCarousel({
    autoPlay: 3000, //Set AutoPlay to 5 seconds
    autoplay: true,
    smartSpeed: 2000, // Default is 250
    items : 4,
    loop:true,
    margin:30,
    touchDrag: true,
    mouseDrag: true,
    pagination:false,
    nav:false,
    dots: false,
        responsive: {
            1200: {
                items: 4
            },
            992: {
                items: 4
            },
            768: {
                items: 3
            },
            480: {
                items: 2
            },
            320: {
                items: 1
            },
            280: {
                items: 1
            }
        }
  });


})(jQuery);