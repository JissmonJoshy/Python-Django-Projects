$(document).ready(function(){
    initCounter();
    initNavLink();
    initSidebar()
    initSidebarDropdown();
    initProgressBar();
    initSubmitAppointment();
    initSubmitNewsletter();
    initGalleryFilter();
});

function initCounter() {
    var $counters = $(".counter");

    function updateCount($counter) {
        var target = +$counter.data("target");
        var count = +$counter.text();
        var duration = 1000;
        var steps = 30;
        var increment = Math.max(1, Math.ceil(target / steps));
        var delay = Math.floor(duration / (target / increment));

        if (count < target) {
            var nextCount = Math.min(target, count + increment);
            $counter.text(nextCount);
            setTimeout(function() {
                updateCount($counter);
            }, delay);
        } else {
            $counter.text(target);
        }
    }

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting && !$(entry.target).data('counted')) {
                var $counter = $(entry.target);
                $counter.data('counted', true);
                updateCount($counter);
            }
        });
    }, {
        threshold: 0.5
    });

    $counters.each(function() {
        var $counter = $(this);
        $counter.data('counted', false);
        observer.observe(this);
    });
}


function initProgressBar(){
    $(document).ready(function () {
        const $bars = $(".progress-bar");
    
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const $bar = $(entry.target);
                    const target = $bar.data("progress-target");
                    const $textEl = $bar.find(".progress-text");
    
                    $bar.css("width", target + "%");
    
                    let current = 0;
                    const step = Math.ceil(target / 30);
    
                    const timer = setInterval(() => {
                        current += step;
                        if (current >= target) {
                            current = target;
                            clearInterval(timer);
                        }
                        $textEl.text(current + "%");
                    }, 30);
    
                    obs.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.4
        });
    
        $bars.each(function() {
            observer.observe(this);
        });
    });
}

function initNavLink() {
    const currentUrl = window.location.href;
    $(".navbar-nav .nav-link").each(function() {
        if (this.href === currentUrl) {
            $(this).addClass("active");
        }
    });
    $(".navbar-nav .dropdown-menu .dropdown-item").each(function() {
        if (this.href === currentUrl) {
            $(this).addClass("active");
            $(this).closest(".dropdown").find(".nav-link.dropdown-toggle").addClass("active");
        }
    });
}

function initSidebar() {
    const $menuBtn = $('.nav-btn');
    const $closeBtn = $('.close-btn');
    const $overlay = $('.sidebar-overlay');
    const $sidebar = $('.sidebar');
  
    $menuBtn.click(function() {
      $overlay.addClass('active');
      setTimeout(() => {
        $sidebar.addClass('active');
      }, 200);
    });
  
    $closeBtn.click(function() {
      $sidebar.removeClass('active');
      setTimeout(() => {
        $overlay.removeClass('active');
      }, 200);
    });
  
    $overlay.click(function() {
      $sidebar.removeClass('active');
      setTimeout(() => {
        $overlay.removeClass('active');
      }, 200);
    });
}

function initSidebarDropdown() {
    const $dropdownButtons = $(".sidebar-dropdown-btn");

    $dropdownButtons.each(function() {
        $(this).on("click", function() {
            const $dropdownMenu = $(this).parent().next(".sidebar-dropdown-menu");
            const isOpen = $dropdownMenu.hasClass("active");

            $(".sidebar-dropdown-menu").not($dropdownMenu).removeClass("active");

            $dropdownMenu.toggleClass("active", !isOpen);
        });
    });
}

function initGalleryFilter() {
    const $tabs = $(".gallery-tab");
    const $items = $(".gallery-item");

    if (!$tabs.length || !$items.length) return;

    $tabs.on("click", function() {
        $tabs.removeClass("active");
        $(this).addClass("active");

        const filter = $(this).data("filter");

        $items.each(function() {
            const $item = $(this);
            const category = $item.data("category");

            // Sembunyikan semua dulu
            if (filter === "all" || category === filter) {
                $item.removeClass("hidden");

                // reset animasi
                $item.removeClass("fade-in");
                void this.offsetWidth; // trik untuk restart animation

                // apply animasi
                $item.addClass("fade-in");

            } else {
                $item.addClass("hidden");
            }
        });
    });
}
