/*
Theme Name: 
Version: 
Author: 
Author URI: 
Description: 
*/
/*	IE 10 Fix*/

(function ($) {
	'use strict';
	
	jQuery(document).ready(function () {


        // Isotope Portfolio
        var iso = $grid.data('isotope');
        var $filterCount = $('.filter-count');

        // bind filter button click
        $('.filters-button-group .button').on( 'click', function() {
            var filterValue = $( this ).attr('data-filter');
            // use filterFn if matches value
            $grid.isotope({ filter: filterValue });
            updateFilterCount();
        });

        function updateFilterCount() {
            $filterCount.text( iso.filteredItems.length);
        }
        updateFilterCount();

        // change is-checked class on buttons
        $('.filters-button-group').each( function( i, buttonGroup ) {
            var $buttonGroup = $( buttonGroup );
            $buttonGroup.on( 'click', 'button', function() {
                $buttonGroup.find('.is-checked').removeClass('is-checked');
                $( this ).addClass('is-checked');
            });
		});

		

		$grid.imagesLoaded().progress( function() {
			$grid.isotope('layout');
		});
		
		//****************************
		// Isotope Load more button
		//****************************
		var initShow = 9; 
		var counter = initShow;
		loadMore(initShow);
		function loadMore(toShow) {
			$grid.find(".hidden").removeClass("hidden");

			var hiddenElems = iso.filteredItems.slice(toShow, iso.filteredItems.length).map(function(item) {
				return item.element;
			});
			$(hiddenElems).addClass('hidden');
			$grid.isotope('layout');

			if (hiddenElems.length == 0) {
				jQuery("#load-more").hide();
			} else {
				jQuery("#load-more").show();
			};

		}

		//append load more button
		// $grid.after('<button id="load-more" class="btn btn-dark">Load More</button>');
		//when load more button clicked
		$("#load-more").click(function() {
			if ($('.filters-button-group').data('clicked')) {
				counter = initShow;
				$('.filters-button-group').data('clicked', false);
			} else {
				counter = counter;
			};
			counter = counter + initShow;
			loadMore(counter);
		});

		//when filter button clicked
		$(".filters-button-group").click(function() {
			$(this).data('clicked', true);

			loadMore(initShow);
		});
    

		$(function() {
			$(' .grid-item ').each( function() { $(this).hoverdir(); } );
		});

 	});	
})(jQuery);

var $grid = $('.grid').isotope({
	itemSelector: '.grid-item', 
	percentPosition: true,
	layoutMode: 'masonry',
	transformsEnabled: true,
	transitionDuration: "700ms",
	resize: true,
	fitWidth: true,
	columnWidth: '.grid-sizer',
});