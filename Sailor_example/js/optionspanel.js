jQuery(document).ready(function($) {
	
	$('.options_toggle').bind('click', function() {
		if($('#t_options').css('left') == '0px'){
			$('#t_options').stop(false, true).animate({left:'-230px'}, 400, 'easeOutExpo');
		}else {
			$('#t_options').stop(false, true).animate({left:'0px'}, 400, 'easeOutExpo');
		}	
	});

	$(".wideboxed a.wrapboxed").click(function() { 
		$.cookie($('#wrapper').addClass("boxed"));
		return false;
	});
	$(".wideboxed a.wrapwide").click(function() { 
		$.cookie($('#wrapper').removeClass("boxed"));
		return false;
	});
	
	
	$("#stylechanger .color a").click(function() { 
		$("#t-colors").attr("href",'skins/'+$(this).attr('data-rel'));
		$.cookie("css",'skins/'+$(this).attr('data-rel'), {expires: 365, path: '/'});
		return false;
	});
	
	$(".bgr .color a").click(function() { 
		$("#bodybg").attr("href",'bodybg/'+$(this).attr('data-rel'));
		$.cookie("css",'bodybg/'+$(this).attr('data-rel'), {expires: 365, path: '/'});
		return false;
	});
	
	$('#accent_color').ColorPicker({
		onSubmit: function(hsb, hex, rgb, el) {
			$(el).val(hex);
			$(el).ColorPickerHide();
		},
		onBeforeShow: function () {
			$(this).ColorPickerSetColor(this.value);
		},
		onChange: function (hsb, hex, rgb) {
			$('#accent_color').val(hex);
			$('#accent_color').css('backgroundColor', '#' + hex);
			accentColorUpdate(hex);
		}
	})
	.bind('keyup', function(){
		$(this).ColorPickerSetColor(this.value);
	});
	
	$('#bodybg_color').ColorPicker({
		onSubmit: function(hsb, hex, rgb, el) {
			$(el).val(hex);
			$(el).ColorPickerHide();
		},
		onBeforeShow: function () {
			$(this).ColorPickerSetColor(this.value);
		},
		onChange: function (hsb, hex, rgb) {
			$('#bodybg_color').val(hex);
			$('#bodybg_color').css('backgroundColor', '#' + hex);
			bodybgColorUpdate(hex);
		}
	})
	.bind('keyup', function(){
		$(this).ColorPickerSetColor(this.value);
	});
	
function accentColorUpdate(hex){

	hex = '#'+hex;

	$('#custom_styles').html('<style>'+
		'	a, a:hover,a:focus,a:active, strike, .post-meta span a:hover,ul.meta-post li a:hover, ul.cat li a:hover, ul.recent li h6 a:hover, ul.portfolio-categ li.active a, ul.portfolio-categ li.active a:hover, ul.portfolio-categ li a:hover,ul.related-post li h4 a:hover, span.highlight,article .post-heading h3 a:hover,.navbar .nav > .active > a,.navbar .nav > .active > a:hover,.navbar .nav > li > a:hover,.navbar .nav > li > a:focus,.navbar .nav > .active > a:focus, .validation,.navbar-brand span,header .nav li a:hover,header .nav li a:focus,header .nav li.active a,header .nav li.active a:hover,header .nav li a.dropdown-toggle:hover,header .nav li a.dropdown-toggle:focus,header .nav li.active ul.dropdown-menu li a:hover,header .nav li.active ul.dropdown-menu li.active a { color:'+ hex +'; }' +
		'	.navbar-default .navbar-nav > .active > a,.navbar-default .navbar-nav > .active > a:hover,.navbar-default .navbar-nav > .active > a:focus,.navbar-default .navbar-nav > .open > a,.navbar-default .navbar-nav > .open > a:hover,.navbar-default .navbar-nav > .open > a:focus,.dropdown-menu > .active > a,.dropdown-menu > .active > a:hover,.dropdown-menu > .active > a:focus  { color:'+ hex +';}'+
		'	#sendmessage,.cta-text h2 span,.post-meta .comments a:hover ,.recent-post .text h5 a:hover,.cbp-l-filters-alignCenter .cbp-filter-item:hover,.cbp-l-filters-alignCenter .cbp-filter-item-active  { color: '+ hex +';}'+
		'	textarea:focus,.form-control:focus,input[type="text"]:focus,input[type="password"]:focus,input[type="datetime"]:focus,input[type="datetime-local"]:focus,input[type="date"]:focus,input[type="month"]:focus,input[type="time"]:focus,input[type="week"]:focus,input[type="number"]:focus,input[type="email"]:focus,input[type="url"]:focus,input[type="search"]:focus,input[type="tel"]:focus,input[type="color"]:focus,.uneditable-input:focus,input:focus,.cbp-l-filters-list .cbp-filter-item{ border-color: '+ hex +';}'+
		
	    '   .pagination ul > li.active > a,.pagination ul > li.active > span, a.thumbnail:hover, input[type="text"].search-form:focus,.btn-dark:hover,.btn-dark:focus,.btn-dark:active,.btn-theme,.cbp-l-filters-alignLeft .cbp-filter-item-active { border:1px solid '+ hex +'; }'+
		' .cbp-l-filters-button .cbp-filter-counter:before,.post-meta   { border-top: 4px solid '+ hex +';}'+
		' .pullquote-left,#featured .flexslider .slide-caption { border-left: 5px solid '+ hex +';}'+
		' .pullquote-right  { border-right: 5px solid '+ hex +';}'+
		' ul.clients li:hover,.da-slide .da-link:hover { border: 4px solid '+ hex +';}'+
		' .nivo-caption, .caption  { border-bottom: 5px solid '+ hex +';}'+
		
	    '  .highlight,.custom-carousel-nav.right:hover, .custom-carousel-nav.left:hover,.pagination ul > .active > a:hover,.pagination ul > .active > a,.pagination ul > .active > span,.flex-control-nav li a:hover,.flex-control-nav li a.active,.cbp-l-caption-buttonLeft,.cbp-l-caption-buttonRight,.cbp-l-filters-button .cbp-filter-counter,.breadcrumb,.modal.styled .modal-header,.cbp-l-filters-alignLeft .cbp-filter-item-active,.cbp-l-filters-list .cbp-filter-item-active ,.cbp-popup-singlePage .cbp-popup-navigation-wrap,.cbp-popup-singlePage .cbp-l-project-details-visit{ background-color: '+ hex +';}'+

	    '  .icon-square:hover,.icon-rounded:hover,.icon-circled:hover,[class^="icon-"].active,[class*=" icon-"].active,.fancybox-close:hover  { background-color: '+ hex +';}'+

	    ' .sb-icon-search,.btn-dark:hover,.btn-dark:focus,.btn-dark:active,.btn-theme,.widget ul.tags li a:hover,.pricing-box-alt.special .pricing-heading,.cbp-l-filters-dropdownWrap,.cbp-l-filters-alignRight .cbp-filter-counter,#pagination a:hover,.pricing-box.special .pricing-offer { background: '+ hex +';}'+

		'	#featured .flexslider .slide-caption { border-left: 5px solid '+ hex +';}'+
		'	.nivo-caption, .caption { border-bottom: 5px solid '+ hex +';}'+
		
		'</style>');
}

function bodybgColorUpdate(hex){
	$('body').css('background', '#'+hex);
}
	
});