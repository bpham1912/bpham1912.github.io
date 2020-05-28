var $ = jQuery.noConflict();
$(document).ready(function() {

	"use strict";

	/*-----------------------------------------------------------------------------------*/
	/*  Superfish Menu
	/*-----------------------------------------------------------------------------------*/
	var example = $('ul.sf-menu').superfish({
		delay:       100,
		speed:       'fast',
		autoArrows:  false
	});

	/*-----------------------------------------------------------------------------------*/
	/*  Scroll Top
	/*-----------------------------------------------------------------------------------*/
	$.scrollUp({
		scrollText: '<i class="fa fa-chevron-up"></i>'
	});

	/*-----------------------------------------------------------------------------------*/
	/*  Slick Nav
	/*-----------------------------------------------------------------------------------*/
	$('#primary-menu').slicknav({
		prependTo:'#primary-bar',
		label: "Menu"
	});
	$('#secondary-menu').slicknav({
		prependTo:'#secondary-bar',
		label: "Browse"
	});

	/*-----------------------------------------------------------------------------------*/
	/*  bxSlidser
	/*-----------------------------------------------------------------------------------*/
	$('.bxslider').bxSlider({
		onSliderLoad: function(){
			$(".bxslider-wrap").css("visibility", "visible");
		},
		prevText: "<i class='fa fa-chevron-left'></i>",
		nextText: "<i class='fa fa-chevron-right'></i>"
	});

	/*-----------------------------------------------------------------------------------*/
	/*  Fitvids
	/*-----------------------------------------------------------------------------------*/
	$(".hentry, .widget").fitVids();

	/*-----------------------------------------------------------------------------------*/
	/*  Masonry
	/*-----------------------------------------------------------------------------------*/

	var grid_width = setGridWidth();

	// for debugging
	// console.log(grid_width);

	var $grid =	$('.grid').masonry({
		// options
		itemSelector: '.grid-item',
		columnWidth: grid_width,
		gutter: 20
	});

	$grid.imagesLoaded().progress( function() {
		$grid.masonry('layout');
	});

	$(window).resize(function () {
		grid_width = setGridWidth();

		// for debugging
		// console.log(grid_width);

		$('.grid').masonry({
			columnWidth: grid_width,
		});
	});


	/*-----------------------------------------------------------------------------------*/
	/*  Tabs Widget
	/*-----------------------------------------------------------------------------------*/
	var $tabsNav    = $('.tabs-nav'),
		$tabsNavLis = $tabsNav.children('li'),
		$tabContent = $('.tab-content');

	$tabsNav.each(function() {
		var $this = $(this);

		$this.next().children('.tab-content').stop(true,true).hide()
											 .first().show();

		$this.children('li').first().addClass('active').stop(true,true).show();
	});

	$tabsNavLis.on('click', function(e) {
		var $this = $(this);

		$this.siblings().removeClass('active').end()
			 .addClass('active');

		$this.parent().next().children('.tab-content').stop(true,true).hide()
													  .siblings( $this.find('a').attr('href') ).fadeIn();

		e.preventDefault();
	});

	/*-----------------------------------------------------------------------------------*/
	/*  WebFont
	/*-----------------------------------------------------------------------------------*/
	WebFont.load({
	google: {
		families: ['Roboto', 'sans-serif']
	}
	});

	/*-----------------------------------------------------------------------------------*/
	/*  Infinite Scroll
	/*-----------------------------------------------------------------------------------*/

	var $container = $('.content-loop');
		$container.infinitescroll({
			navSelector  : '#page-nav',    // selector for the paged navigation
			nextSelector : '#page-nav a',  // selector for the NEXT link (to page 2)
			itemSelector : '.grid-item',   // selector for all items you'll retrieve
			loading: {
				msgText: '',
				finishedMsg: '',
				img: 'assets/img/bx_loader.gif'
			}
		},
		// trigger Masonry as a callback
		function( newElements ) {
			var $newElems = $( newElements );
			$newElems.imagesLoaded( function() {
				$('.hentry').fitVids();
				$('.bxslider').bxSlider({
					onSliderLoad: function(){
						$(".bxslider-wrap").css("visibility", "visible");
					},
					prevText: "<i class='fa fa-chevron-left'></i>",
					nextText: "<i class='fa fa-chevron-right'></i>"
				});
				$container.masonry( 'appended', $newElems );
			});
		}
	);

});


// for use in Masonry
function setGridWidth() {

	var set_width = $(window).width();
	// initial width for three-columns
	var grid_width = 346;

	/* Standard Desktop Screen */
	if(set_width > 1119) {
		if( $('body').hasClass('four-columns') ) {
			grid_width = 255;
		} else if( $('body').hasClass('two-columns') ) {
			grid_width = 530;
		} else if( $('body').hasClass('one-column') ) {
			grid_width = 1080;
		} else {
			grid_width = 346;
		}
	}

	/* Small Desktop Screen */
	if ((set_width > 959) && (set_width < 1120)) {
		if( $('body').hasClass('two-columns') ) {
			grid_width = 450;
		} else if( $('body').hasClass('one-column') ) {
			grid_width = 920;
		} else {
			grid_width = 293;
		}
	}

	/* Tablet Screen */
	if ((set_width > 767) && (set_width < 960)) {
		if( $('body').hasClass('one-column') ) {
			grid_width = 738;
		} else {
			grid_width = 359;
		}
	}

	/* Mobile Phone and Small Tablet Screen */
	if ((set_width > 479) && (set_width < 768)) {
		grid_width = 460;
	}

	return grid_width;

}
