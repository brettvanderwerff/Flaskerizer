/*global jQuery:false */
jQuery(document).ready(function($) {
  "use strict";


  //add some elements with animate effect

  $(".big-cta").hover(
    function() {
      $('.cta a').addClass("animated shake");
    },
    function() {
      $('.cta a').removeClass("animated shake");
    }
  );
  $(".box").hover(
    function() {
      $(this).find('.icon').addClass("animated fadeInDown");
      $(this).find('p').addClass("animated fadeInUp");
    },
    function() {
      $(this).find('.icon').removeClass("animated fadeInDown");
      $(this).find('p').removeClass("animated fadeInUp");
    }
  );


  $('.accordion').on('show', function(e) {

    $(e.target).prev('.accordion-heading').find('.accordion-toggle').addClass('active');
    $(e.target).prev('.accordion-heading').find('.accordion-toggle i').removeClass('icon-plus');
    $(e.target).prev('.accordion-heading').find('.accordion-toggle i').addClass('icon-minus');
  });

  $('.accordion').on('hide', function(e) {
    $(this).find('.accordion-toggle').not($(e.target)).removeClass('active');
    $(this).find('.accordion-toggle i').not($(e.target)).removeClass('icon-minus');
    $(this).find('.accordion-toggle i').not($(e.target)).addClass('icon-plus');
  });


  //register/login form
  $(function() {
    $('.button-checkbox').each(function() {

      // Settings
      var $widget = $(this),
        $button = $widget.find('button'),
        $checkbox = $widget.find('input:checkbox'),
        color = $button.data('color'),
        settings = {
          on: {
            icon: 'glyphicon glyphicon-check'
          },
          off: {
            icon: 'glyphicon glyphicon-unchecked'
          }
        };

      // Event Handlers
      $button.on('click', function() {
        $checkbox.prop('checked', !$checkbox.is(':checked'));
        $checkbox.triggerHandler('change');
        updateDisplay();
      });
      $checkbox.on('change', function() {
        updateDisplay();
      });

      // Actions
      function updateDisplay() {
        var isChecked = $checkbox.is(':checked');

        // Set the button's state
        $button.data('state', (isChecked) ? "on" : "off");

        // Set the button's icon
        $button.find('.state-icon')
          .removeClass()
          .addClass('state-icon ' + settings[$button.data('state')].icon);

        // Update the button's color
        if (isChecked) {
          $button
            .removeClass('btn-default')
            .addClass('btn-' + color + ' active');
        } else {
          $button
            .removeClass('btn-' + color + ' active')
            .addClass('btn-default');
        }
      }

      // Initialization
      function init() {

        updateDisplay();

        // Inject the icon if applicable
        if ($button.find('.state-icon').length == 0) {
          $button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i> ');
        }
      }
      init();
    });
  });


  // tooltip
  $('.social-network li a, .options_box .color a').tooltip();


  //stats
  jQuery('.appear').appear();
  var runOnce = true;
  jQuery(".stats").on("appear", function(data) {
    var counters = {};
    var i = 0;
    if (runOnce) {
      jQuery('.number').each(function() {
        counters[this.id] = $(this).html();
        i++;
      });
      jQuery.each(counters, function(i, val) {
        //console.log(i + ' - ' +val);
        jQuery({
          countNum: 0
        }).animate({
          countNum: val
        }, {
          duration: 3000,
          easing: 'linear',
          step: function() {
            jQuery('#' + i).text(Math.floor(this.countNum));
          }
        });
      });
      runOnce = false;
    }
  });

  //parallax
  if ($('.parallax').length) {
    $(window).stellar({
      responsive: true,
      scrollProperty: 'scroll',
      parallaxElements: false,
      horizontalScrolling: false,
      horizontalOffset: 0,
      verticalOffset: 0
    });

  }



  //scroll to top
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      $('.scrollup').fadeIn();
    } else {
      $('.scrollup').fadeOut();
    }
  });
  $('.scrollup').click(function() {
    $("html, body").animate({
      scrollTop: 0
    }, 1000);
    return false;
  });




  //search
  if( $('#sb-search').length ) {
    new UISearch(document.getElementById('sb-search'));
  }

  //cube portfolio
  var gridContainer = $('#grid-container'),
    filtersContainer = $('#filters-container');

  // init cubeportfolio
  gridContainer.cubeportfolio({

    defaultFilter: '*',

    animationType: 'flipOutDelay',

    gapHorizontal: 45,

    gapVertical: 30,

    gridAdjustment: 'responsive',

    caption: 'overlayBottomReveal',

    displayType: 'lazyLoading',

    displayTypeSpeed: 100,

    // lightbox
    lightboxDelegate: '.cbp-lightbox',
    lightboxGallery: true,
    lightboxTitleSrc: 'data-title',
    lightboxShowCounter: true

  });

  // add listener for filters click
  filtersContainer.on('click', '.cbp-filter-item', function(e) {

    var me = $(this),
      wrap;

    // get cubeportfolio data and check if is still animating (reposition) the items.
    if (!$.data(gridContainer[0], 'cubeportfolio').isAnimating) {

      if (filtersContainer.hasClass('cbp-l-filters-dropdown')) {
        wrap = $('.cbp-l-filters-dropdownWrap');

        wrap.find('.cbp-filter-item').removeClass('cbp-filter-item-active');

        wrap.find('.cbp-l-filters-dropdownHeader').text(me.text());

        me.addClass('cbp-filter-item-active');
      } else {
        me.addClass('cbp-filter-item-active').siblings().removeClass('cbp-filter-item-active');
      }

    }

    // filter the items
    gridContainer.cubeportfolio('filter', me.data('filter'), function() {});

  });

  // activate counters
  gridContainer.cubeportfolio('showCounter', filtersContainer.find('.cbp-filter-item'));


  // add listener for load more click
  $('.cbp-l-loadMore-button-link').on('click', function(e) {

    e.preventDefault();

    var clicks, me = $(this),
      oMsg;

    if (me.hasClass('cbp-l-loadMore-button-stop')) return;

    // get the number of times the loadMore link has been clicked
    clicks = $.data(this, 'numberOfClicks');
    clicks = (clicks) ? ++clicks : 1;
    $.data(this, 'numberOfClicks', clicks);

    // set loading status
    oMsg = me.text();
    me.text('LOADING...');

    // perform ajax request
    $.ajax({
        url: me.attr('href'),
        type: 'GET',
        dataType: 'HTML'
      })
      .done(function(result) {
        var items, itemsNext;

        // find current container
        items = $(result).filter(function() {
          return $(this).is('div' + '.cbp-loadMore-block' + clicks);
        });

        gridContainer.cubeportfolio('appendItems', items.html(),
          function() {
            // put the original message back
            me.text(oMsg);

            // check if we have more works
            itemsNext = $(result).filter(function() {
              return $(this).is('div' + '.cbp-loadMore-block' + (clicks + 1));
            });

            if (itemsNext.length === 0) {
              me.text('NO MORE WORKS');
              me.addClass('cbp-l-loadMore-button-stop');
            }

          });

      })
      .fail(function() {
        // error
      });

  });

});
