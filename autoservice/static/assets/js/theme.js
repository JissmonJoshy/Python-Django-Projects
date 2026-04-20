/*
Theme Name: Ducatibox - Car Service & Auto Repair Template
Version: 1.0
Author: WPThemeBooster
Author URL: 
Description: Ducatibox - Car Service & Auto Repair Template
*/
/*	IE 10 Fix*/

(function ($) {
	'use strict';
	
	jQuery(document).ready(function () {

        // Preloader
        setTimeout(function() {
            $('#preloader').addClass('hide');
        }, 1000);

        // Add Menu Item Current Class Auto
        function dynamicCurrentMenuClass(selector) {
            let FileName = window.location.href.split("/").reverse()[0];
  
            selector.find("li").each(function () {
              let anchor = $(this).find("a");
              if ($(anchor).attr("href") == FileName) {
                $(this).addClass("active");
              }
            });
            // if any li has .current elmnt add class
            selector.children("li").each(function () {
              if ($(this).find(".active").length) {
                $(this).addClass("active");
              }
            });
            // if no file name return
            if ("" == FileName) {
              selector.find("li").eq(0).addClass("active");
            }
        }
          
        if ($('.mainnav .main-menu').length) {
            dynamicCurrentMenuClass($('.mainnav .main-menu'));
        }

        // Mobile Responsive Menu 
        var mobileLogoContent = $('header .logo').html();
        var mobileMenuContent = $('.mainnav').html();
		$('.mr_menu .logo').append(mobileLogoContent);
		$('.mr_menu .mr_navmenu').append(mobileMenuContent);
        $( '.mr_menu .mr_navmenu ul.main-menu li.menu-item-has-children').append( $( "<span class='submenu_opener'><i class='bi bi-chevron-right'></i></span>" ) );

        // Sub-Menu Open On-Click
        $('.mr_menu ul.main-menu li.menu-item-has-children .submenu_opener').on("click", function(e){
            $(this).parent().toggleClass('nav_open');
            $(this).siblings('ul').slideToggle();
            e.stopPropagation();
            e.preventDefault();
        });
        
        // Active Mobile Responsive Menu : Add Class in body tag
        $('.mr_menu_toggle').on('click', function(e) {
            $('body').addClass('mr_menu_active');
            e.stopPropagation();
            e.preventDefault();
        });
        $('.mr_menu_close').on('click', function(e) {
            $('body').removeClass('mr_menu_active');
            e.stopPropagation();
            e.preventDefault();
        });
        
        // $('body').on('click', function(e) {
        //     $('body').removeClass('mr_menu_active');
        //     e.stopPropagation();
        //     e.preventDefault();
        // });


        // Aside info bar
        $('.aside_open').on("click", function(e) {
            e.preventDefault();
            $(this).addClass('close');
            $('.aside_info_wrapper').addClass('show');
        });
        $('.aside_close').on("click", function(e) {
            e.preventDefault();
            $('.aside_open').removeClass('close');
            $('.aside_info_wrapper').removeClass('show');
        });

        // Toggle Header Search
        $('.header_search .form-control-submit').on("click", function() {
            $('.open_search').toggleClass('active');
        });

        // Sticky Header
        var header = $("header");
        $(window).scroll(function() {
            var scroll = $(window).scrollTop();

            if (scroll >= 50) {
                header.addClass("sticky");
            } else {
                header.removeClass("sticky");
            }
        });


        // WOW Init
        new WOW().init();

        // Swiper Start

        // Main Slider One
        var SwiperSlider = new Swiper('.swiper-main-slider', {
            loop: true,
            // autoplay: {
            //     delay: 4000,
            // },
            autoHeight: true,
            speed: 2500,
            slidesPerView: 1,
            spaceBetween: 0,            
            // navigation: {
            //     nextEl: '.swiper-button-next',
            //     prevEl: '.swiper-button-prev',
            // },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
        });

        // Main Slider Two
        var SwiperSlider2 = new Swiper('.style2 .swiper-main-slider', {
            loop: true,
            // autoplay: {
            //     delay: 4000,
            // },
            autoHeight: true,
            speed: 2500,
            slidesPerView: 1,
            spaceBetween: 0,            
            // navigation: {
            //     nextEl: '.swiper-button-next',
            //     prevEl: '.swiper-button-prev',
            // },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                renderBullet: function (index, className) {
                    return '<span class="' + className + '">' + '<span class="number">' + (index + 1) + "</span>" + "</span>";
                },
            },
        });

        // Imagebox One
        var SwiperImagebox = new Swiper('.swiper-imagebox', {
            loop: true,
            autoplay: {
                delay: 4000,
            },
            speed: 1500,
            slidesPerView: 1,
            spaceBetween: 0,            
            // navigation: {
            //     nextEl: '.swiper-button-next',
            //     prevEl: '.swiper-button-prev',
            // },
            pagination: {
                el: '.swiper-pagination',
                clickable: true
            },
            breakpoints: {
                600: {
                  slidesPerView: 2,
                },
                992: {
                  slidesPerView: 3,
                },
                1400: {
                  slidesPerView: 4,
                },
            }
        });

        // Testimonial One
        var SwiperTestimonial = new Swiper('.swiper-testimonial', {
            loop: true,
            autoplay: {
                delay: 4000,
            },
            speed: 1500,
            slidesPerView: 1,
            spaceBetween: 30,            
            // navigation: {
            //     nextEl: '.swiper-button-next',
            //     prevEl: '.swiper-button-prev',
            // },
            pagination: {
                el: '.swiper-pagination',
                clickable: true
            },
            breakpoints: {
                768: {
                  slidesPerView: 1,
                },
            }
        });

        // Testimonial Two
        var SwiperTestimonialTwo = new Swiper('.swiper-testimonial2', {
            loop: true,
            // autoplay: {
            //     delay: 4000,
            // },
            speed: 1500,
            slidesPerView: 1,
            spaceBetween: 30,            
            // navigation: {
            //     nextEl: '.swiper-button-next',
            //     prevEl: '.swiper-button-prev',
            // },
            pagination: {
                el: '.swiper-pagination',
                clickable: true
            },
            breakpoints: {
                768: {
                  slidesPerView: 1,
                },

                1200: {
                    slidesPerView: 3,
                  },
            }
        });

        // Clients Logo One
        var SwiperClients = new Swiper('.swiper-clients', {
            loop: true,
            autoplay: {
                delay: 4000,
            },
            speed: 1500,
            slidesPerView: 1,
            spaceBetween: 30,            
            // navigation: {
            //     nextEl: '.swiper-button-next',
            //     prevEl: '.swiper-button-prev',
            // },
            pagination: {
                el: '.swiper-pagination',
                clickable: true
            },
            breakpoints: {
                400: {
                  slidesPerView: 2,
                },
                576: {
                    slidesPerView: 3,
                },
                992: {
                    slidesPerView: 5,
                },
            }
        });

        // Clients Logo Two
        var SwiperClients = new Swiper('.swiper-clients2', {
            loop: true,
            autoplay: {
                delay: 4000,
            },
            speed: 1500,
            slidesPerView: 1,
            spaceBetween: 0,            
            // navigation: {
            //     nextEl: '.swiper-button-next',
            //     prevEl: '.swiper-button-prev',
            // },
            pagination: {
                el: '.swiper-pagination',
                clickable: true
            },
            breakpoints: {
                400: {
                  slidesPerView: 2,
                },
                576: {
                    slidesPerView: 3,
                },
                992: {
                    slidesPerView: 5,
                },
                1200: {
                    slidesPerView: 6,
                },
            }
        });

        // Blog
        var SwiperBlog = new Swiper('.swiper-blog', {
            loop: true,
            // autoplay: {
            //     delay: 4000,
            // },
            speed: 1500,
            slidesPerView: 1,
            spaceBetween: 30,            
            // navigation: {
            //     nextEl: '.swiper-button-next',
            //     prevEl: '.swiper-button-prev',
            // },
            pagination: {
                el: '.swiper-pagination',
                clickable: true
            },
            breakpoints: {
                768: {
                  slidesPerView: 2,
                },
                992: {
                  slidesPerView: 2,
                },
            }
        });

        // Landing Innerpages
        var SwiperInnerpages = new Swiper('.swiper-innerpages', {
            loop: true,
            autoplay: {
                delay: 4000,
            },
            speed: 1500,
            slidesPerView: 1,
            spaceBetween: 0, 
            breakpoints: {
                600: {
                  slidesPerView: 2,
                },
                992: {
                  slidesPerView: 3,
                  spaceBetween: 30, 
                },
                1400: {
                  slidesPerView: 4,
                  spaceBetween: 40, 
                },
            }
        });


        // Odometer
        $('.odometer').appear();
        $('.odometer').appear(function(){
            var odo = $(".odometer");
            odo.each(function() {
                var countNumber = $(this).attr("data-count");
                $(this).html(countNumber);
            });
            window.odometerOptions = {
                format: 'd',
            };
        });


        // Alternate Hover/Active
        $('.wptb-image-box1, .wptb-image-box2, .wptb-blog-grid1, .wptb-packages1, .wptb-icon-box2').on("mouseenter", function(){     
            $('.wptb-image-box1, .wptb-image-box2, .wptb-blog-grid1, .wptb-packages1, .wptb-icon-box2').removeClass('active');    
        }).on('mouseleave',  function(){ 
            $('.wptb-image-box1.highlight, .wptb-image-box2.highlight, .wptb-blog-grid1.highlight, .wptb-packages1.highlight, .wptb-icon-box2.highlight').addClass('active');     
        });

        // accordion
        $(".wptb-accordion").on("click",".wptb-item-title", function () {
            $(this).next().slideDown();
            $(".wptb-item--content").not($(this).next()).slideUp();
        });

        $(".wptb-accordion").on("click",".wptb--item", function () {
            $(this).addClass("active").siblings().removeClass("active");
        });


        // Radial Progressbar
        function radial_animate() { 
            $('svg.radial-progress').each(function( index, value ) { 
  
                $(this).find($('circle.bar--animated')).removeAttr( 'style' );    
                // Get element in Veiw port
                var elementTop = $(this).offset().top;
                var elementBottom = elementTop + $(this).outerHeight();
                var viewportTop = $(window).scrollTop();
                var viewportBottom = viewportTop + $(window).height();
                
                if(elementBottom > viewportTop && elementTop < viewportBottom) {
                    var percent = $(value).data('countervalue');
                    var radius = $(this).find($('circle.bar--animated')).attr('r');
                    var circumference = 2 * Math.PI * radius;
                    var strokeDashOffset = circumference - ((percent * circumference) / 100);
                    $(this).find($('circle.bar--animated')).animate({'stroke-dashoffset': strokeDashOffset}, 2800);
                }
            });
        }
        // To check If it is in Viewport 
        var $window = $(window);
        function check_if_in_view() {    
            $('.countervalue').each(function(){
                if ($(this).hasClass('start')){
                    var elementTop = $(this).offset().top;
                    var elementBottom = elementTop + $(this).outerHeight();

                    var viewportTop = $(window).scrollTop();
                    var viewportBottom = viewportTop + $(window).height();

                    if (elementBottom > viewportTop && elementTop < viewportBottom) {
                        $(this).removeClass('start');
                        $('.countervalue').text();
                        var myNumbers = $(this).text();
                        if (myNumbers == Math.floor(myNumbers)) {
                            $(this).animate({
                                Counter: $(this).text()
                            }, {
                                duration: 2800,
                                easing: 'swing',
                                step: function(now) {
                                    $(this).text(Math.ceil(now)  + '%');                                
                                }
                            });
                        } else {
                            $(this).animate({
                                Counter: $(this).text()
                            }, {
                                duration: 2800,
                                easing: 'swing',
                                step: function(now) {                                
                                    $(this).text(now.toFixed(2)  + '$'); 
                                }
                            });
                        }

                        radial_animate();
                    }
                }
            });
        }
        $window.on('scroll', check_if_in_view);


        // Fancybox
        $('[data-fancybox="video"]').fancybox({
			arrows: true,
			animationEffect: [
			//"false",            - disable
			//"fade",
			//"slide",
			//"circular",
			//"tube",
			//"zoom-in-out",
			"rotate"
			],
			transitionEffect: [
			//"false",            - disable
			//"fade",
			//"slide",
			"circular",
			//"tube",
			//"zoom-in-out",
			//"rotate"
			],
			buttons: [
			"zoom",
			//"share",
			//"slideShow",
			"fullScreen",
			//"download",
			//"thumbs",
			"close"
			],
			infobar: false,
		});

        // Youtube
        var $ytvideoTrigger = $(".ytplay-btn");
        $ytvideoTrigger.on("click", function(evt) {  
            $(".ytube-video").addClass("play");
            $("#ytvideo")[0].src += "?autoplay=1";
        });

        // Vertical Accordion
          $('.wptb-country-tab--title').on('click', function () {
            $('.wptb-country-tab--item').removeClass('active');
            $(this).parent('.wptb-country-tab--item').addClass('active');
        });

        // Time Counter
        function makeTimer() {
            var endTime = new Date("14 March 2026");      
            endTime = (Date.parse(endTime) / 1000);
    
            var now = new Date();
            now = (Date.parse(now) / 1000);
    
            var timeLeft = endTime - now;
    
            var days = Math.floor(timeLeft / 86400); 
            var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
            var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
            var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
        
            if (hours < "10") { hours = "0" + hours; }
            if (minutes < "10") { minutes = "0" + minutes; }
            if (seconds < "10") { seconds = "0" + seconds; }
    
            $("#days").html(days);
            $("#hours").html(hours);
            $("#minutes").html(minutes);
            $("#seconds").html(seconds);   
        }
        setInterval(function() { makeTimer(); }, 1000);


        // Shop
        // Product Zoom
        $('.product_zoom_button_group > li > a').eq(0).addClass( "selected" );
        $('.product_zoom_container > .product_zoom_info').eq(0).css('display','block');
        $('.product_zoom_button_group').on("click",function(e){
            if($(e.target).is("a")){

                /*Handle Tab Nav*/
                $('.product_zoom_button_group > li > a').removeClass( "selected");
                $(e.target).addClass( "selected");
                
                /*Handles Tab Content*/
                var clicked_index = $("a",this).index(e.target);
                $('.product_zoom_container > .product_zoom_info').css('display','none');
                $('.product_zoom_container > .product_zoom_info').eq(clicked_index).fadeIn();
            }
            $(this).blur();
            return false;
        });

        // Header Cart open
		$('a.wptb-cart-icon').on('click', function (e) {
			e.preventDefault();
			$('.wptb-cart-box').toggleClass('active');
		});

        // Datepickr / Flatpicker
        $(".flatpickr").flatpickr({
            mode: "range",
            dateFormat: "d-M",
            minDate: "today",
        });
        $(".flatpickr-time").flatpickr({
			enableTime: true,
            noCalendar: true,
            dateFormat: 'h:i K'
		});

        // Nice Select
        $('select').niceSelect();

        // Totop Button
        $('.totop a').on('click', function(e) {
            e.preventDefault();
            $('html, body').animate({scrollTop: 0}, '300');
        });

        // Day-Night Mode Switcher
        var icon = document.getElementById("mode_switcher");

        // if (localStorage.getItem("theme") === "null"){
        //     localStorage.setItem("theme", "light");
        // }

        // let localData = localStorage.getItem("theme");

        // if (localData === "light") {
        //     icon.innerHTML = '<span><i class="bi bi-moon-fill"></i></span>';
        //     document.body.classList.remove("theme-style--light");
        // } else if (localData === "dark"){
        //     icon.innerHTML = '<span><i class="bi bi-sun-fill"></i></span>';
        //     document.body.classList.add("theme-style--light");
        // }

        icon.onclick = function() {
            document.body.classList.toggle("theme-style--light");
            if (document.body.classList.contains("theme-style--light")){
                icon.innerHTML = '<span><i class="bi bi-sun-fill"></i></span>';
                localStorage.setItem("theme", "dark");
            } else {
                icon.innerHTML = '<span><i class="bi bi-moon-fill"></i></span>';
                localStorage.setItem("theme", "light");
            }
        }

    });      
})(jQuery);

// Hide header on scroll down
const nav = document.querySelector(".header");
const scrollUp = "top-up";
let lastScroll = 800;

window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll <= 800) {
        nav.classList.remove(scrollUp);
        $('.totop').removeClass('show');
        return;
    }
    
    if (currentScroll > lastScroll) {
        // down
        nav.classList.add(scrollUp);
        $('.totop').addClass('show');
    } else if (currentScroll < lastScroll) {
        // up
        nav.classList.remove(scrollUp);
        $('.totop').removeClass('show');
    }
    lastScroll = currentScroll;
});


