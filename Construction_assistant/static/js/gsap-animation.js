gsap.registerPlugin(ScrollTrigger, SplitText);
gsap.config({
    nullTargetWarn: false,
    trialWarn: false
});
/*----  Functions  ----*/
function pbmit_img_animation() {
    const boxes = gsap.utils.toArray('.pbmit-animation-style1,.pbmit-animation-style2,.pbmit-animation-style3,.pbmit-animation-style4,.pbmit-animation-style5,.pbmit-animation-style6,.pbmit-animation-style7');
    boxes.forEach(img => {
        gsap.to(img, {
            scrollTrigger: {
                trigger: img,
                start: "top 70%",
                end: "bottom bottom",
                toggleClass: "active",
                once: true,
            }
        });
    });
}

function getpercentage(x, y, elm) { 
    elm.find('.pbmit-fid-inner').html(y + '/' + x);
    var cal = Math.round((y * 100) / x);
    return cal;
}

function pbmit_title_animation() {

	ScrollTrigger.matchMedia({
		"(min-width: 1025px)": function() {

		var pbmit_var = jQuery('.pbmit-heading, .pbmit-heading-subheading');
		if (!pbmit_var.length) {
			return;
		}
		const quotes = document.querySelectorAll(".pbmit-heading-subheading .pbmit-title, .pbmit-heading .pbmit-title");

			quotes.forEach(quote => {

				//Reset if needed
				if (quote.animation) {
					quote.animation.progress(1).kill();
					quote.split.revert();
				}

				var getclass = quote.closest('.pbmit-heading-subheading, .pbmit-heading').className;
				var animation = getclass.split('animation-');
				if (animation[1] == "style4") return

				quote.split = new SplitText(quote, {
					type: "lines,words,chars",
					linesClass: "split-line"
				});
				gsap.set(quote, { perspective: 400 });

				if (animation[1] == "style1") {
					gsap.set(quote.split.chars, {
						opacity: 0,
						y: "90%",
						rotateX: "-40deg"
					});
				}
				if (animation[1] == "style2") {
					gsap.set(quote.split.chars, {
						opacity: 0,
						x: "50"
					});
				}
				if (animation[1] == "style3") {
					gsap.set(quote.split.chars, {
						opacity: 0,
					});
				}
				quote.animation = gsap.to(quote.split.chars, {
					scrollTrigger: {
						trigger: quote,
						start: "top 90%",
					},
					x: "0",
					y: "0",
					rotateX: "0",
					opacity: 1,
					duration: 1,
					ease: Back.easeOut,
					stagger: .02
				});
			});
		},
	});
}

var pbmit_animation_number_rotate = function() {
	jQuery('.odometer').each(function() {
		var self = jQuery(this);
		self.waypoint(function(direction) {
			var v = self.data('to');
			self.html(v);
		}, { offset: '85%' });
	});
}

// ** Hover Image Effect ** \\
function pbmit_hover_img() {
	const pbmitHoverImg = gsap.utils.toArray(".pbmit-element-service-style-3 article");
	pbmitHoverImg.forEach((target) => {
		const pbmitImg = target.querySelector('.pbmit-hover-img');
		const t1 = gsap.timeline();
		t1.to(pbmitImg, {
			opacity: 1,
			duration: 0.4,
			scale: 1,
			ease: "Power2.easeOut"
		})
		target.pbmitHoverAnim = t1.play().reversed(true);
		target.addEventListener("mouseenter", pbmithoverimg);
		target.addEventListener("mouseleave", pbmithoverimg);
		target.addEventListener("mousemove", (e) => {
			let xpos = e.offsetX;
			let ypos = e.offsetY;
			const t1 = gsap.timeline();
			t1.to(pbmitImg, { x: xpos, y: ypos });
		});
	});

	function pbmithoverimg() {
		this.pbmitHoverAnim.reversed(!this.pbmitHoverAnim.reversed());
	}
}

function pbmit_verticel_layered_pinning() {
	var pbmit_var = jQuery('.pbmit-element-portfolio-style-4');
	if (!pbmit_var.length) {
		return;
	}
	ScrollTrigger.matchMedia({
		"(min-width: 992px)": function() {

			let pbmitpanels = gsap.utils.toArray(".pbmit-element-portfolio-style-4 .pbminfotech-box-content");
			const spacer = 100;
		
			let pbmitheight = pbmitpanels[0].offsetHeight + 0;
			pbmitpanels.forEach((pbmitpanel, i) => {
			ScrollTrigger.create({
				trigger: pbmitpanel,
				start: () => "top 0px", 
				endTrigger: '.pbmit-element-portfolio-style-4', 
				end: `bottom top+=${pbmitheight + (pbmitpanels.length * spacer)}`,
				pin: true, 
				pinSpacing: false, 
			});
			});
		},
		"(max-width:992px)": function() {
			ScrollTrigger.getAll().forEach(pbmitpanels => pbmitpanels.kill(true));
		}
	});
}

function pbmit_tween_effect() {

	const pbmit_tween = gsap.utils.toArray('.pbmit-tween-effect');
	if (pbmit_tween.length == 0) return

	ScrollTrigger.matchMedia({
		"(min-width: 1200px)": function() {

			pbmit_tween.forEach((box, i) => {
				let tl = gsap.timeline({
					scrollTrigger: {
						trigger: box,
						start: "top 90%",
						end: "bottom 70%",
						scrub: 1
					},
					defaults: { ease: "none" }
				});

				let xpos_val = box.getAttribute('data-x-start');
				let xpose_val = box.getAttribute('data-x-end');
				let ypos_val = box.getAttribute('data-y-start');
				let ypose_val = box.getAttribute('data-y-end');

				let scale_x_val = box.getAttribute('data-scale-x-start');
				let scale_xe_val = box.getAttribute('data-scale-x-end');

				let skew_x_val = box.getAttribute('data-skew-x-start');
				let skew_xe_val = box.getAttribute('data-skew-x-end');
				let skew_y_val = box.getAttribute('data-skew-y-start');
				let skew_ey_val = box.getAttribute('data-skew-y-end');

				let rotation_x_val = box.getAttribute('data-rotate-x-start');
				let rotation_xe_val = box.getAttribute('data-rotate-x-end');
				gsap.set(box, { xPercent: xpos_val, yPercent: ypos_val, scale: scale_x_val, skewX: skew_x_val, skewY: skew_y_val, rotation: rotation_x_val });
				tl.to(box, { xPercent: xpose_val, yPercent: ypose_val, scale: scale_xe_val, skewX: skew_xe_val, skewY: skew_ey_val, rotation: rotation_xe_val })
			});
		},
		"(max-width:1200px)": function() {
			ScrollTrigger.getAll().forEach(box => box.kill(true));
		}
	});
}

var pbmit_multi_icon_box_hover_effect = function() {
	jQuery(".pbmit-multi-icon-box-hover-effect .pbmit-miconheading-style-1:nth-child(2),.pbmit-multi-icon-box-hover-effect .pbmit-miconheading-style-3:nth-child(2)").eq(0).addClass('pbmit-mihbox-hover-active');
	jQuery(".pbmit-multi-icon-box-hover-effect .pbmit-miconheading-style-1,.pbmit-multi-icon-box-hover-effect .pbmit-miconheading-style-3").mouseover(function() {
		var main_row = jQuery(this).closest('.pbmit-multi-icon-box-hover-effect');
		jQuery('.pbmit-miconheading-style-1,.pbmit-miconheading-style-3', main_row).removeClass('pbmit-mihbox-hover-active');
		jQuery(this).addClass('pbmit-mihbox-hover-active');
	}).mouseout(function() {
		var main_row = jQuery(this).closest('.pbmit-multi-icon-box-hover-effect');
		jQuery('.pbmit-miconheading-style-1,.pbmit-miconheading-style-3', main_row).removeClass('pbmit-mihbox-hover-active');
		jQuery(this).addClass('pbmit-mihbox-hover-active');
	});
}

var pbmit_active_hover = function() {

	var pbmit_var = jQuery('.pbmit-element-blog-style-4,.pbmit-element-portfolio-style-2,.pbmit-element-portfolio-style-3,.pbmit-element-service-style-4,.pbmit-element-static-box-style-1,.pbmit-element-static-box-style-2');

	if (!pbmit_var.length) {
		return;
	}

	pbmit_var.each(function() {
		var pbmit_Class = '.pbmit-hover-inner li,.pbmit-blog-style-4,.swiper-hover-slide-nav .swiper-slide,.pbmit-service-style-4,.pbmit-content-box.col-md-3,.pbmit-card-box-wrapper';
		jQuery(this)
			.find(pbmit_Class).first()
			.addClass('pbmit-active');
		jQuery(this)
			.find(pbmit_Class)
			.on('mouseover', function() {
				jQuery(this).addClass('pbmit-active').siblings().removeClass('pbmit-active');
			});
	});
}

function pbmit_mousehover_tooltip() {

	jQuery("<div id='pbmit-portfolio-cursor'><div class='pbmit-tooltip-content'></div></div>").appendTo("body");

	var pbmit_text = jQuery('.pbmit-element-portfolio-style-3 .pbminfotech-post-content');
	var pbmit_cursor = jQuery("#pbmit-portfolio-cursor");

	jQuery(document).on('mousemove', function(e) {
		var pbmit_x = e.clientX;
		var pbmit_y = e.clientY;
		pbmit_cursor.css({ "transform": "translate3d(" + pbmit_x + "px, " + pbmit_y + "px, 0px)" });
	})

	if (pbmit_text.length) {
		pbmit_text.each(function() {
			var elm = jQuery(this);
			var pbmit_html = elm.find('.pbminfotech-box-content').html();
			elm.on('mouseenter', function() {
				pbmit_cursor.addClass('active').find('.pbmit-tooltip-content').html(pbmit_html);
			}).on('mouseleave', function(e) {
				pbmit_cursor.removeClass('active').find('.pbmit-tooltip-content').html('');
			});
		});
	}
}

function pbmit_portfolio3_slider() {
	jQuery(".pbmit-element-portfolio-style-3").each(function() {

		if (typeof Swiper !== 'undefined') {

			var pbmit_port_slide = new Swiper('.swiper-hover-slide-nav', {
				spaceBetween: 0,
				autoplay :false,
				loop:true,
				slidesPerView: '1',
				navigation: {
					nextEl: '.swiper-button-next',
					prevEl: '.swiper-button-prev',
				},
				breakpoints	: {
					1025: {
						slidesPerView: '4',
					},
					767: {
						slidesPerView: '3',
					},
					575: {
						slidesPerView: '2',
					},
				},
			});
			var pbmit_hover_fade1 = new Swiper(".pbmit-hover-image-faded", {
				speed: 6000,
				effect: 'fade',
			});
			jQuery('.pbmit-main-hover-faded .swiper-hover-slide-nav .swiper-slide').on('mouseover',function(e) {
				e.preventDefault();
				var myindex = jQuery(this).attr('data-swiper-slide-index');
				pbmit_hover_fade1.slideTo(myindex, 2000, false);
			});
		}
	});		
}

/* Static Box style1 Slide */
var pbmit_staticbox_hover_slide = function() {
	if (typeof Swiper !== 'undefined') {
		var pbmit_hover1 = new Swiper(".pbmit-static-image", {
			grabCursor: true,
			effect: "slide",
			allowTouchMove: false
		});
		var pbmit_hover2 = new Swiper(".pbmit-hover-number", {
			grabCursor: true,
			effect: "creative",
			creativeEffect: {
				prev: {
					translate: [0, "-170%", 1],
				},
				next: {
					translate: [0, "100%", 0],
				},
			},
			allowTouchMove: false
		});
		jQuery('.pbmit-main-static-slider li').on('mouseover',function(e) {
			e.preventDefault();
			var myindex = jQuery(this).index();
			pbmit_hover1.slideTo(myindex, 500, false);
			pbmit_hover2.slideTo(myindex, 500, false);
		});
	}
}

function pbmit_extend_section() {
	const pbmit_elm = gsap.utils.toArray('.pbmit-extend-animation');
	if (pbmit_elm.length == 0) return	
	ScrollTrigger.matchMedia({
		"(min-width: 1200px)": function() {
			 
			pbmit_elm.forEach(section => {
				let tl = gsap.timeline({
					scrollTrigger: {
						trigger: section,
						start: "top 50%",
						end: "+=400px",
						scrub: 1
					},
					defaults: { ease: "none" }
				});
				tl.fromTo(section, { clipPath: 'inset(0% 6% 0% 6% )' }, { clipPath: 'inset(0% 0% 0% 0% )', duration: 1.5 })	
			});			 
		},
		"(max-width:1200px)": function() {
			ScrollTrigger.getAll().forEach(section => section.kill(true));
		}
	});
}

function pbmit_animate_custom_text() {
	jQuery("#js-rotating").Morphext({
		animation: "flipInX",
		speed: 3000,
	});
}

// function pbmit_ihbox_move() {

// 	var pbmit_var = jQuery('.pbmit-move-sofa');
// 	if (!pbmit_var.length) {
// 		return;
// 	}
// 	ScrollTrigger.matchMedia({
// 		"(min-width: 1200px)": function() {

// 			gsap.set(".pbmit-move-sofa", { yPercent:20, })

// 			gsap.to(".pbmit-move-sofa", {		
// 				yPercent: -50,
// 				scrollTrigger: {
// 					scrub: true,
// 					start: () => "top top", 
// 					end:() =>  "bottom top",
// 					scrub:2
// 				}
// 			});
// 		},
// 		"(max-width:1200px)": function() {
// 			ScrollTrigger.getAll().forEach(scrub => scrub.kill(true));
// 		}
// 	});
// }

function pbmit_sticky() {

	ScrollTrigger.matchMedia({
		"(min-width: 1201px)": function() {
			let pbmit_sticky_container = jQuery(".pbmit-sticky-col");
			let section = pbmit_sticky_container.closest('.section');
			if (!section[0]) {
				section = pbmit_sticky_container.closest('.pbmit-sticky-section');
			} 
			let tl = gsap.timeline({
				scrollTrigger: {
					pin: pbmit_sticky_container,
					scrub: 1,
					start: "top top", 
					trigger: section,
					end: () => "+=" + ((section.height() + 250) - window.innerHeight), 
					invalidateOnRefresh: true
				},
				defaults: { ease: "none", duration: 1 }
			});
		},
	}); 
}

function pbmit_coverflow_testimonial() {
	if (!jQuery('.pbmit-element-testimonial-style-4').length) {
		return;
	}
	var pbmit_coverflow = new Swiper('.pbmit-element-testimonial-style-4 .pbmit-coverflow', {
		loop: true,
		speed: 1000,
		autoplay: {
			delay: 3000,
		},
		effect: 'coverflow',
		grabCursor: true,
		centeredSlides: false,
		spaceBetween:30,
		slidesPerView: '1',	
		coverflowEffect: {
			rotate: 0,
			stretch: 0,
			depth: 300,
			slideShadows: false,
		},
		breakpoints	: {
			575: {
				slidesPerView: '2',
				centeredSlides: true,
			},
		},
	});		
}

function pbmit_scale_video() {

	var pbmit_var = jQuery('.pbmit-element-video-scale-style-1');
	if (!pbmit_var.length) {
		return;
	}

	ScrollTrigger.matchMedia({
		"(min-width: 1200px)": function() {

			const pbmit_scale = gsap.timeline({		
			scrollTrigger: {
				trigger	: ".pbmit-video-wrapper",
				scrub	: 0.8,
				start	: "top bottom",
				end		: "bottom top",
				ease	: "power5.out"
			}
			});
			pbmit_scale.to(".pbmit-video-wrapper", {
			duration	: 1,
			scale		: 1.5,
			});
			gsap.set(".pbmit-element-video-scale-style-1 .pbmit-ele-header-area", { yPercent: 50 });
			gsap.to(".pbmit-element-video-scale-style-1 .pbmit-ele-header-area", {
				yPercent: 280,
				scrollTrigger: {
					trigger	: ".pbmit-element-video-scale-style-1 .pbmit-ele-header-area",
					scrub	: 0.8,
					start	: "top top",
					end		: "center",
					ease	: "power5.out",
					
				}
			});
		},
		"(max-width:1200px)": function() {
			ScrollTrigger.getAll().forEach(scrollTrigger => scrollTrigger.kill(true));
		}	
	});
}

var pbmit_hover_slide = function() {
	if (typeof Swiper !== 'undefined') {
		var pbmit_hover_slide = new Swiper(".pbmit-hover-image", {
			grabCursor: true,
			effect: "slide",
			allowTouchMove: false,
			mousewheel: false,
		});		
	}
	jQuery('.pbmit-main-hover-slider li').on('mouseover',function(e) {
		e.preventDefault();
		var myindex = jQuery(this).index();
		pbmit_hover_slide.slideTo(myindex, 500, false);
	});
}

function pbmit_card_verticel_pinning() {
	var pbmit_var = jQuery('.pbmit-element-card-box-style-1');
	if (!pbmit_var.length) {
		return;
	}
	ScrollTrigger.matchMedia({
		"(min-width: 992px)": function() {

			let pbmitpanels = gsap.utils.toArray(".pbmit-element-card-box-style-1 .pbmit-card-box-wrapper");
			const spacer = 0;
		
			let pbmitheight = pbmitpanels[0].offsetHeight + 120;
			pbmitpanels.forEach((pbmitpanel, i) => {
			ScrollTrigger.create({
				trigger: pbmitpanel, 
				start: () => "top 100px", 
				endTrigger: '.pbmit-element-card-box-style-1', 
				end: `bottom top+=${pbmitheight + (pbmitpanels.length * spacer)}`,
				pin: true, 
				pinSpacing: false, 
			});
			});
		},
		"(max-width:992px)": function() {
			ScrollTrigger.getAll().forEach(pbmitpanels => pbmitpanels.kill(true));
		}
	});
}

// function pbmit_sticky_special() {
// 	if (jQuery('.pbmit-sticky-col2-special').hasClass('.elementor-element-edit-mode')) {
// 		return;
// 	}
// 	ScrollTrigger.matchMedia({
// 		"(min-width: 1024px)": function() { 
// 			let pbmit_sticky_2 = jQuery(".pbmit-sticky-col2-special");
// 			let section = jQuery('.pbmit-sticky-special'); 
// 			let section_height = pbmit_sticky_2.height();
// 			const tweenOne = gsap.to(pbmit_sticky_2, {
// 				y: - (section_height - 600),
// 				scrollTrigger: {
// 				  trigger: section,
// 				  pin: section,
// 				  scrub: true,
// 				  start: "top top+=140px",
// 				  end: () => '+=' + (section_height - 600),
// 				}
// 			}); 
// 		},
// 		"(max-width:1024px)": function() {
// 			ScrollTrigger.getAll().forEach(section => section.kill(true));
// 		}
// 	}); 
// }

function pbmit_set_tooltip() {
    $('[data-cursor-tooltip]').each(function() {
        var thisele = $(this);
        var thisele_html = thisele.find('.pbminfotech-box-content').html();
        thisele.attr("data-cursor-tooltip", thisele_html);
    });
}

// function pbmit_staticbox_hover() {
// 	var pbmit_var = jQuery('.pbmit-element-static-box-style-1');
// 	if (!pbmit_var.length) {
// 		return;
// 	}
// 	pbmit_var.each(function() {
// 		var pbmit_Class = '.swiper-static-slide-nav .pbmit-hover-inner li ';
// 		jQuery(this)
// 			.find(pbmit_Class).first()
// 			.addClass('pbmit-active');
// 		jQuery(this)
// 			.find(pbmit_Class)
// 			.on('mouseover', function() {
// 				jQuery(this).addClass('pbmit-active').siblings().removeClass('pbmit-active');
// 			});
// 	});
// }

/* Static Box Slider */
// var pbmit_staticbox_hover_slide = function() {
// 	if (typeof Swiper !== 'undefined') {
// 		var pbmit_hover = new Swiper(".pbmit-hover-image-faded", {
// 			speed: 6000,
// 			effect: 'fade',
// 		});
// 		var pbmit_hover1 = new Swiper(".pbmit-hover-short-desc", {
// 			grabCursor: true,
// 			effect: "creative",
// 			creativeEffect: {
// 				prev: {
// 					translate: [0, "-170%", 1],
// 				},
// 				next: {
// 					translate: [0, "100%", 0],
// 				},
// 			},
// 			allowTouchMove: false
// 		});
// 		jQuery('.pbmit-main-static-slider li').on('mouseover', function(e) {
// 			e.preventDefault();
// 			var myindex = jQuery(this).index();
// 			pbmit_hover.slideTo(myindex, 1000, false);
// 			pbmit_hover1.slideTo(myindex, 500, false);
// 		});
// 	}
// }

// function pbmit_img_animation() {
// 	const boxes = gsap.utils.toArray('.pbmit-animation-style1,.pbmit-animation-style2,.pbmit-animation-style3,.pbmit-animation-style4,.pbmit-animation-style5,.pbmit-animation-style6,.pbmit-animation-style7');
// 	boxes.forEach(img => {
// 		gsap.to(img, {
// 			scrollTrigger: {
// 				trigger: img,
// 				start: "top 70%",
// 				end: "bottom bottom",
// 				toggleClass: "active",
// 				once: true,
// 			}
// 		});
// 	});
// }

ScrollTrigger.matchMedia({
    "(max-width: 1200px)": function() {
        ScrollTrigger.getAll().forEach(t => t.kill());
    }
});

// on ready
jQuery(document).ready(function() {
	pbmit_animation_number_rotate();
	pbmit_title_animation();
	pbmit_verticel_layered_pinning();
	pbmit_multi_icon_box_hover_effect();
	pbmit_active_hover();
	pbmit_portfolio3_slider();
	pbmit_staticbox_hover_slide();
	pbmit_coverflow_testimonial();
	pbmit_scale_video();
	pbmit_hover_slide();
	// pbmit_staticbox_hover();
	// pbmit_staticbox_hover_slide();
});

// on resize
jQuery(window).resize(function() {
	pbmit_title_animation();
	pbmit_img_animation();
	pbmit_mousehover_tooltip();
});

// on load
jQuery(window).on('load', function(){
	// pbmit_sticky_special();
	pbmit_hover_img();
	pbmit_animate_custom_text();
	pbmit_img_animation();
	pbmit_tween_effect();
	pbmit_extend_section();
	pbmit_sticky();
	pbmit_card_verticel_pinning();
	
	jQuery('[data-magnetic]').each(function() { new Magnetic(this); });
	gsap.delayedCall(1, () =>
		ScrollTrigger.getAll().forEach((t) => {
			t.refresh();
		})
	);	
	
	setTimeout(cleaning, 500);
	function cleaning(){
		ScrollTrigger.refresh(); 
	}
});