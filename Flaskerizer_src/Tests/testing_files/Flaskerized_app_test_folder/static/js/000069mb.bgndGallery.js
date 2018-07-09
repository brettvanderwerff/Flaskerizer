/*___________________________________________________________________________________________________________________________________________________
 _ jquery.mb.components                                                                                                                             _
 _                                                                                                                                                  _
 _ file: jquery.mb.bgndGallery.src.js                                                                                                               _
 _ last modified: 21/06/15 15.53                                                                                                                    _
 _                                                                                                                                                  _
 _ Open Lab s.r.l., Florence - Italy                                                                                                                _
 _                                                                                                                                                  _
 _ email: matteo@open-lab.com                                                                                                                       _
 _ site: http://pupunzi.com                                                                                                                         _
 _       http://open-lab.com                                                                                                                        _
 _ blog: http://pupunzi.open-lab.com                                                                                                                _
 _ Q&A:  http://jquery.pupunzi.com                                                                                                                  _
 _                                                                                                                                                  _
 _ Licences: MIT, GPL                                                                                                                               _
 _    http://www.opensource.org/licenses/mit-license.php                                                                                            _
 _    http://www.gnu.org/licenses/gpl.html                                                                                                          _
 _                                                                                                                                                  _
 _ Copyright (c) 2001-2015. Matteo Bicocchi (Pupunzi);                                                                                              _
 ___________________________________________________________________________________________________________________________________________________*/

( function( jQuery ) {

	jQuery.mbBgndGallery = {
		name: "mb.bgndGallery",
		author: "Matteo Bicocchi",
		version: "1.9.5",
		build: "2459",

		clear: false,
		defaults: {
			containment: "body",
			images: [],
			shuffle: false,
			controls: null,
			effect: "fade",
			filter: null,
			timer: 4000,
			effTimer: 5000,
			raster: false,
			folderPath: false,
			autoStart: true,
			grayScale: false,
			activateKeyboard: true,
			preserveTop: false,
			preserveWidth: false,
			placeHolder: "",

			//Path to the folder containing the thumbnails and ID of the DOM element that should contains them.
			// Thumbnail should have the same name of the corresponding image
			thumbs: {
				folderPath: "",
				placeholder: ""
			},

			onStart: function() {},
			onChange: function( opt, idx ) {},
			onPause: function( opt ) {},
			onPlay: function( opt ) {},
			onNext: function( opt ) {},
			onPrev: function( opt ) {}

			// idx = the zero based index of the displayed photo
			// opt=the options relatives to this component instance you can manipulate on the specific event

			// for example, if you want to reverse the enter/exit effect once the previous button is clicked:
			// you can change the opt.effect onPrev event : opt.effect = "slideRight"
			// onNext:function(opt){opt.effect = "slideLeft"}
			// onPrev:function(opt){opt.effect = "slideRight"}

		},

		buildGallery: function( options ) {
			var opt = {};
			jQuery.extend( opt, jQuery.mbBgndGallery.defaults, options );
			var el = jQuery( opt.containment ).get( 0 );
			el.opt = opt;
			el.opt.galleryID = new Date().getTime();
			jQuery.mbBgndGallery.el = el;
			if( el.opt.onStart )
				el.opt.onStart();

			el.opt.gallery = jQuery( "<div/>" ).attr( {
				id: "bgndGallery_" + el.opt.galleryID
			} ).addClass( "mbBgndGallery" );
			var pos = el.opt.containment == "body" ? "fixed" : "absolute";
			var css = {
				position: pos,
				top: 0,
				let: 0,
				width: "100%",
				height: "100%",
				overflow: "hidden",
				"-webkit-transform-style": "flat",
				"-webkit-transform": "translateZ(0)",
				"z-index": 0
			};
			el.opt.gallery.css( css );

			var containment = el.opt.containment;

			if( containment != "body" && jQuery( containment ).text().trim() != "" ) {
				var wrapper = jQuery( "<div/>" ).css( {
					"position": "absolute",
					minHeight: "100%",
					minWidth: "100%",
					zIndex: 3
				} );
				jQuery( containment ).wrapInner( wrapper );
				if( jQuery( containment ).css( "position" ) == "static" )
					jQuery( containment ).css( "position", "relative" );
			}

			var raster = jQuery( "<div/>" ).css( {
				position: "absolute",
				top: 0,
				left: 0,
				width: "100%",
				height: "100%",
				zIndex: 1
			} ).addClass( opt.raster ? "bgg_raster" : "" );
			el.opt.gallery.append( raster );

			jQuery( containment ).prepend( opt.gallery );

			if( el.opt.folderPath && el.opt.images.length == 0 )
				el.opt.images = jQuery.loadFromSystem( el.opt.folderPath );

			if( el.opt.shuffle )
				el.opt.images = jQuery.shuffle( el.opt.images );

			var totImg = el.opt.images.length;

			var loadCounter = 0;

			jQuery.mbBgndGallery.preload( el.opt.images[ 0 ], el );
			el.opt.gallery.on( "imageLoaded." + el.opt.galleryID, function() {
				loadCounter++;
				if( loadCounter == totImg ) {
					el.opt.gallery.off( "imageLoaded." + el.opt.galleryID );
					return;
				}
				jQuery.mbBgndGallery.preload( el.opt.images[ loadCounter ], el );
			} );

			el.opt.imageCounter = 0;

			jQuery.mbBgndGallery.changePhoto( el.opt.images[ el.opt.imageCounter ], el );

			if( !el.opt.autoStart ) {
				el.opt.paused = true;
				jQuery( el.opt.gallery ).trigger( "paused" );
			}

			el.opt.gallery.on( "imageReady." + el.opt.galleryID, function() {

				if( el.opt.paused )
					return;

				clearTimeout( el.opt.changing );

				jQuery.mbBgndGallery.play( el );
			} );

			jQuery( window ).on( "resize", function() {
				var image = jQuery( "img", el.opt.gallery );
				jQuery.mbBgndGallery.checkSize( image, el );
			} );

			var controls = el.opt.controls;
			if( controls ) {
				jQuery( controls ).addClass( "controls" );

				var counter = jQuery( el.opt.controls ).find( ".counter" );
				counter.html( el.opt.imageCounter + 1 + " / " + el.opt.images.length );

				jQuery.mbBgndGallery.buildControls( controls, el );
				jQuery( el.opt.containment ).on( "paused", function() {
					jQuery( el.opt.controls ).find( ".play" ).show();
					jQuery( el.opt.controls ).find( ".pause" ).hide();
				} );
				jQuery( el.opt.containment ).on( "play", function() {
					jQuery( el.opt.controls ).find( ".play" ).hide();
					jQuery( el.opt.controls ).find( ".pause" ).show();
				} );
			}

			if( el.opt.activateKeyboard )
				jQuery.mbBgndGallery.keyboard( el );

			//	if(el.opt.thumbs.folderPath.trim().length > 0 && el.opt.thumbs.placeholder.trim().length > 0)
			jQuery.mbBgndGallery.buildThumbs( el );

			return jQuery( el );

		},

		preload: function( url, el ) {
			if( jQuery.mbBgndGallery.clear ) {
				el.opt.gallery.remove();
				return;
			}

			var img = jQuery( "<img/>" ).load( function() {
				el.opt.gallery.trigger( "imageLoaded." + el.opt.galleryID );
			} ).attr( "src", url );

		},

		checkSize: function( image, el ) {
			if( !image )
				return;

			if( jQuery.mbBgndGallery.changing )
				return;

			if( jQuery.mbBgndGallery.clear ) {
				el.opt.gallery.remove();
				return;
			}

			return image.each( function() {
				var image = jQuery( this );
				var w = image.attr( "w" );
				var h = image.attr( "h" );

				var containment = el.opt.containment == "body" ? window : el.opt.containment;
				var aspectRatio = w / h;
				var wAspectRatio = jQuery( containment ).width() / jQuery( containment ).height();
				if( aspectRatio >= wAspectRatio ) {
					image.css( "height", "100%" );
					image.css( "width", "auto" );
				} else {
					image.css( "width", "100%" );
					image.css( "height", "auto" );
				}
				image.css( "margin-left", ( ( jQuery( containment ).width() - image.width() ) / 2 ) );

				if( !el.opt.preserveTop )
					image.css( "margin-top", ( ( jQuery( containment ).height() - image.height() ) / 2 ) );

				if( el.opt.preserveWidth ) {
					image.css( {
						width: "100%",
						height: "auto",
						left: 0,
						marginLeft: 0
					} );
				}
			} );
		},

		changePhoto: function( url, el ) {

			if( !document.hasFocus() ) {
				jQuery( window ).one( "focus", function() {
					jQuery.mbBgndGallery.changePhoto( url, el );
				} );
				return;
			}

			if( jQuery.mbBgndGallery.clear ) {
				el.opt.gallery.remove();
				return;
			}

			jQuery.mbBgndGallery.buildThumbs( el );

			if( el.opt.thumbs.folderPath.trim().length > 0 && el.opt.thumbs.placeholder.trim().length > 0 ) {
				jQuery( ".sel", jQuery( el.opt.thumbs.placeholder ) ).removeClass( "sel" );
				jQuery( "#mbBgImg_" + el.opt.imageCounter ).addClass( "sel" );
			}

			jQuery.mbBgndGallery.changing = true;

			clearTimeout( el.opt.changing );

			if( el.opt.onChange )
				el.opt.onChange( el.opt, el.opt.imageCounter );

			var image = jQuery( "<img/>" ).hide().load( function() {

				var that = jQuery( this );

				var tmp = jQuery( "<div/>" ).css( {
					position: "absolute",
					top: -5000
				} );
				tmp.append( that );
				jQuery( "body" ).append( tmp );
				that.attr( "w", that.width() );
				that.attr( "h", that.height() );
				tmp.remove();

				el.opt.effect = typeof el.opt.effect == "object" ? el.opt.effect : jQuery.mbBgndGallery.effects[ el.opt.effect ];

				jQuery( "img", el.opt.gallery ).CSSAnimate( el.opt.effect.exit, el.opt.effTimer, 0, el.opt.effect.exitTiming, function() {

					if( jQuery( this ).length )
						jQuery( this ).remove();

				} );
				that.css( {
					position: "absolute"
				} );

				el.opt.gallery.css( {

					"-webkit-backface-visibility": "none",
					"-webkit-transform-style": "preserve-3d",
					"-webkit-perspective": 1000

				} );

				el.opt.gallery.append( that );

				jQuery.mbBgndGallery.changing = false;
				jQuery.mbBgndGallery.checkSize( that, el );

				var displayProperties = {};
				for( var x in el.opt.effect.enter ) {
					displayProperties[ x ] = 0;
				}

				if( el.opt.filter && !jQuery.browser.mozilla )
					jQuery.extend( displayProperties, el.opt.filter );

				displayProperties.opacity = 1;
				displayProperties.scale = 1;

				that.css3( el.opt.effect.enter ).show().CSSAnimate( displayProperties, el.opt.effTimer, 0, el.opt.effect.enterTiming, function() {
					el.opt.gallery.trigger( "imageReady." + el.opt.galleryID );
				} );

			} ).attr( "src", url );

			image.error( function() {
				var image = jQuery( this );
				image.attr( "src", el.opt.placeHolder );
			} );

			var counter = jQuery( el.opt.controls ).find( ".counter" );
			counter.html( el.opt.imageCounter + 1 + " / " + el.opt.images.length );

		},

		play: function( el ) {

			if( !el )
				el = this.get( 0 );

			clearTimeout( el.opt.changing );

			var imgToRemove = jQuery( "img", el.opt.gallery ).not( ":last" );
			imgToRemove.remove();

			if( jQuery.mbBgndGallery.clear ) {
				el.opt.gallery.remove();
				return;
			}

			if( el.opt.onPlay )
				el.opt.onPlay( el.opt );

			el.opt.changing = setTimeout( function() {
				if( el.opt.paused )
					return;

				if( el.opt.onNext )
					el.opt.onNext( el.opt );

				if( el.opt.imageCounter >= el.opt.images.length - 1 )
					el.opt.imageCounter = -1;

				el.opt.imageCounter++;

				jQuery.mbBgndGallery.changePhoto( el.opt.images[ el.opt.imageCounter ], jQuery( el.opt.containment ).get( 0 ) );

			}, el.opt.paused ? 0 : el.opt.timer );

			el.opt.gallery.trigger( "play" );

		},

		pause: function( el ) {

			if( !el )
				el = this.get( 0 );

			if( jQuery.mbBgndGallery.clear ) {
				el.opt.gallery.remove();
				return;
			}

			clearTimeout( el.opt.changing );
			el.opt.paused = true;
			el.opt.gallery.trigger( "paused" );

			if( el.opt.onPause )
				el.opt.onPause( el.opt );

		},

		next: function( el ) {

			if( !el )
				el = this.get( 0 );

			if( jQuery.mbBgndGallery.clear ) {
				el.opt.gallery.remove();
				return;
			}

			if( el.opt.onNext )
				el.opt.onNext( el.opt );

			jQuery.mbBgndGallery.pause( el );

			if( el.opt.imageCounter == el.opt.images.length - 1 )
				el.opt.imageCounter = -1;

			el.opt.imageCounter++;

			jQuery.mbBgndGallery.changePhoto( el.opt.images[ el.opt.imageCounter ], el );
			clearTimeout( el.opt.changing );

		},

		prev: function( el ) {

			if( !el )
				el = this.get( 0 );

			if( jQuery.mbBgndGallery.clear ) {
				el.opt.gallery.remove();
				return;
			}

			if( el.opt.onPrev )
				el.opt.onPrev( el.opt );

			jQuery.mbBgndGallery.pause( el );

			clearTimeout( el.opt.changing );
			if( el.opt.imageCounter == 0 )
				el.opt.imageCounter = el.opt.images.length;

			el.opt.imageCounter--;

			jQuery.mbBgndGallery.changePhoto( el.opt.images[ el.opt.imageCounter ], el );

		},

		loader: {
			show: function() {},
			hide: function() {}
		},

		keyboard: function( el ) {

			jQuery( document ).off( "keydown.bgndGallery" ).on( "keydown.bgndGallery", function( e ) {

				if( jQuery( e.target ).is( "textarea" ) || jQuery( e.target ).is( "input" ) || jQuery( e.target ).is( "[contenteditable]" ) )
					return;

				switch( e.keyCode ) {
					case 32:

						if( el.opt.paused ) {

							jQuery.mbBgndGallery.play( el );
							el.opt.paused = false;

						} else {

							el.opt.paused = true;
							jQuery.mbBgndGallery.pause( el );

						}

						e.preventDefault();
						break;

					case 39: // NEXT

						jQuery.mbBgndGallery.next( el );
						e.preventDefault();
						break;

					case 37: //PREV

						jQuery.mbBgndGallery.prev( el );
						e.preventDefault();
						break;

				}
			} )
		},

		buildControls: function( controls, el ) {

			var pause = jQuery( controls ).find( ".pause" );
			var play = jQuery( controls ).find( ".play" );
			var next = jQuery( controls ).find( ".next" );
			var prev = jQuery( controls ).find( ".prev" );
			var fullScreen = jQuery( controls ).find( ".fullscreen" );

			if( ( jQuery.browser.msie || jQuery.browser.opera || 'ontouchstart' in window ) )
				fullScreen.remove();

			if( el.opt.autoStart )
				play.hide();

			pause.on( "click", function() {
				jQuery.mbBgndGallery.pause( el );
				jQuery( this ).hide();
				play.show();
			} );

			play.on( "click", function() {

				if( !el.opt.paused ) return;
				clearTimeout( el.opt.changing );
				jQuery.mbBgndGallery.play( el );
				el.opt.paused = false;

			} );

			next.on( "click", function() {

				jQuery.mbBgndGallery.next( el );
				pause.hide();
				play.show();

			} );

			prev.on( "click", function() {

				jQuery.mbBgndGallery.prev( el );
				pause.hide();
				play.show();

			} );

			fullScreen.on( "click", function() {

				jQuery.mbBgndGallery.runFullscreen( el );

			} );

			if( el.opt.activateKeyboard )
				jQuery.mbBgndGallery.keyboard( el );

		},

		changeGallery: function( array ) {

			var el = this.get( 0 );

			clearTimeout( el.opt.changing );
			el.opt.gallery.off( "imageLoaded." + el.opt.galleryID );

			jQuery.mbBgndGallery.pause( el );
			el.opt.gallery.fadeOut();

			el.opt.images = array;
			el.opt.imageCounter = -1;

			var images = el.opt.images;
			var totImg = images.length;
			var loadCounter = 0;

			jQuery.mbBgndGallery.preload( images[ loadCounter ], el );
			el.opt.gallery.on( "imageLoaded." + el.opt.galleryID, function() {

				if( loadCounter == totImg ) {
					el.opt.gallery.off( "imageLoaded." + el.opt.galleryID );
					el.opt.gallery.fadeIn();
					jQuery.mbBgndGallery.play( el );
					el.opt.paused = false;
					return;
				}

				jQuery.mbBgndGallery.preload( images[ loadCounter ], el );
				loadCounter++;

			} );

			if( el.opt.thumbs.folderPath.trim().length > 0 && el.opt.thumbs.placeholder.trim().length > 0 )
				jQuery.mbBgndGallery.buildThumbs( el );

		},

		changeEffect: function( effect ) {

			jQuery.mbBgndGallery.el.opt.effect = effect;

		},

		runFullscreen: function( el ) {

			if( !el )
				el = this.get( 0 );

			var fullscreenchange = jQuery.browser.mozilla ? "mozfullscreenchange" : jQuery.browser.webkit ? "webkitfullscreenchange" : "fullscreenchange";
			jQuery( document ).off( fullscreenchange );
			jQuery( document ).on( fullscreenchange, function() {
				var isFullScreen = RunPrefixMethod( document, "IsFullScreen" ) || RunPrefixMethod( document, "FullScreen" );

				if( !isFullScreen ) {

					el.isFullscreen = false;

					jQuery( ".fullScreen_controls" ).remove();

					if( !jQuery( el.opt.containment ).is( "body" ) )
						jQuery( el.opt.containment ).css( {
							width: el.width,
							height: el.height,
							top: el.top,
							left: el.left,
							position: el.position
						} );

					el.opt.gallery.css( {
						background: "transparent"
					} );
					var image = jQuery( "#bgndGallery_" + el.opt.galleryID + " img:first" );

				}

				jQuery.mbBgndGallery.checkSize( image, el );

			} );

			if( el.isFullscreen ) {

				cancelFullscreen();

			} else {

				el.isFullscreen = true;

				if( !jQuery( el.opt.containment ).is( "body" ) ) {

					el.width = jQuery( el.opt.containment ).css( "width" );
					el.height = jQuery( el.opt.containment ).css( "height" );
					el.top = jQuery( el.opt.containment ).css( "top" );
					el.left = jQuery( el.opt.containment ).css( "left" );
					el.position = jQuery( el.opt.containment ).css( "position" );

				}

				var controls = jQuery( el.opt.controls ).clone( true ).addClass( "fullScreen_controls" ).css( {
					position: "absolute",
					zIndex: 1000,
					bottom: 20,
					right: 20
				} );
				controls.find( ".fullscreen" ).html( "exit" );
				el.opt.gallery.append( controls ).css( {
					background: "#000"
				} );

				jQuery( el.opt.containment ).CSSAnimate( {

					width: "100%",
					height: "100%",
					top: 0,
					left: 0,
					position: "absolute"

				}, 500 );

				launchFullscreen( el.opt.gallery.get( 0 ) );

			}

			function RunPrefixMethod( obj, method ) {

				var pfx = [ "webkit", "moz", "ms", "o", "" ];
				var p = 0,
					m, t;
				while( p < pfx.length && !obj[ m ] ) {
					m = method;
					if( pfx[ p ] == "" ) {
						m = m.substr( 0, 1 ).toLowerCase() + m.substr( 1 );
					}
					m = pfx[ p ] + m;
					t = typeof obj[ m ];
					if( t != "undefined" ) {
						pfx = [ pfx[ p ] ];
						return( t == "function" ? obj[ m ]() : obj[ m ] );
					}
					p++;
				}

			}

			function launchFullscreen( element ) {
				RunPrefixMethod( element, "RequestFullScreen" );
			}

			function cancelFullscreen() {
				if( RunPrefixMethod( document, "FullScreen" ) || RunPrefixMethod( document, "IsFullScreen" ) ) {
					RunPrefixMethod( document, "CancelFullScreen" );
				}
			}
		},

		buildThumbs: function( el ) {

			if( el.opt.thumbs.folderPath.trim().length == 0 && el.opt.thumbs.placeholder.trim().length == 0 )
				return;

			jQuery( el.opt.thumbs.placeholder ).addClass( "bgg_thumbnailsContainer" );

			function getImageName( path ) {
				return path.split( "/" ).pop();
			}

			var thumbNumber = jQuery( el.opt.thumbs.placeholder ).children().length || 0;

			if( thumbNumber != el.opt.images.length ) {

				jQuery( el.opt.thumbs.placeholder ).empty();
				for( var i = 0; i < el.opt.images.length; i++ ) {

					var imgSrc = el.opt.thumbs.folderPath + getImageName( el.opt.images[ i ] );

					var img = jQuery( "<img/>" ).attr( {
						"src": imgSrc,
						id: "mbBgImg_" + i
					} ).click( function() {
						el.opt.imageCounter = jQuery( this ).attr( "i" ) - 1;
						jQuery.mbBgndGallery.next( el );
						el.opt.paused = true;
					} ).attr( "i", i ).css( {
						opacity: 0
					} ).on( "load", function() {
						jQuery( this ).fadeTo( 1000, 1 );
					} );

					jQuery( el.opt.thumbs.placeholder ).append( img );
				}

				if( el.opt.thumbs.folderPath.trim().length > 0 && el.opt.thumbs.placeholder.trim().length > 0 ) {
					jQuery( ".sel", jQuery( el.opt.thumbs.placeholder ) ).removeClass( "sel" );
					jQuery( "#mbBgImg_" + el.opt.imageCounter ).addClass( "sel" );
				}
			}

		},

		addImages: function( images, goto, shuffle ) {

			var el = this.get( 0 );
			for( var i in images ) {
				el.opt.images.push( images[ i ] );
			}
			if( shuffle )
				el.opt.images = jQuery.shuffle( el.opt.images );

			if( goto )
				el.opt.imageCounter = el.opt.images.indexOf( images[ 0 ] );

			jQuery.mbBgndGallery.buildThumbs( el );

		},

		removeImages: function( images ) {

			var el = this.get( 0 );
			for( var i in images ) {
				var index = el.opt.images.indexOf( images[ i ] );
				if( index > -1 )
					el.opt.images.splice( index, 1 );
			}
			jQuery.mbBgndGallery.changePhoto( el.opt.images[ el.opt.imageCounter ], el );
			jQuery.mbBgndGallery.buildThumbs( el );
		},

		applyFilter: function( filter, val ) {

			var el = this.get( 0 );
			var gallery = el.opt.gallery;
			var f = {};
			f[ filter ] = val;

			gallery.css3( f );

		}
	};

	/**
	 *
	 * Public methods
	 */

	jQuery.fn.mbBgndGalleryPlay = jQuery.mbBgndGallery.play;
	jQuery.fn.mbBgndGalleryPause = jQuery.mbBgndGallery.pause;
	jQuery.fn.mbBgndGalleryPrev = jQuery.mbBgndGallery.prev;
	jQuery.fn.mbBgndGalleryNext = jQuery.mbBgndGallery.next;
	jQuery.fn.changeGallery = jQuery.mbBgndGallery.changeGallery;
	jQuery.fn.addImages = jQuery.mbBgndGallery.addImages;
	jQuery.fn.removeImages = jQuery.mbBgndGallery.removeImages;
	jQuery.fn.applyFilter = jQuery.mbBgndGallery.applyFilter;

	jQuery.loadFromSystem = function( folderPath, type ) {

		// if directory listing is enabled on the remote server.
		// if you run the page locally you need to run it under a local web server (Ex: http://localhost/yourPage)
		// otherwise the directory listing is unavailable.

		if( !folderPath )
			return;
		if( !type )
			type = [ "jpg", "jpeg", "png" ];
		var arr = [];
		jQuery.ajax( {
			url: folderPath,
			async: false,
			success: function( response ) {
				var tmp = jQuery( response );
				var els = tmp.find( "[href]" );

				els.each( function() {
					for( var i in type ) {
						if( jQuery( this ).attr( "href" ).indexOf( type[ i ] ) >= 0 )
							arr.push( folderPath + jQuery( this ).attr( "href" ) );
						arr = jQuery.unique( arr );
					}
				} );
				tmp.remove();
			}
		} );
		return arr.length != 0 ? arr : false;
	};

	jQuery.shuffle = function( arr ) {
		var newArray = arr.slice();
		var len = newArray.length;
		var i = len;
		while( i-- ) {
			var p = parseInt( Math.random() * len );
			var t = newArray[ i ];
			newArray[ i ] = newArray[ p ];
			newArray[ p ] = t;
		}
		return newArray;
	};

} )( jQuery );

function mbBgndGallery( opt ) {
	return jQuery.mbBgndGallery.buildGallery( opt );
}
;/*___________________________________________________________________________________________________________________________________________________
 _ jquery.mb.components                                                                                                                             _
 _                                                                                                                                                  _
 _ file: jquery.mb.bgndGallery.effects.src.js                                                                                                       _
 _ last modified: 27/06/15 17.16                                                                                                                    _
 _                                                                                                                                                  _
 _ Open Lab s.r.l., Florence - Italy                                                                                                                _
 _                                                                                                                                                  _
 _ email: matteo@open-lab.com                                                                                                                       _
 _ site: http://pupunzi.com                                                                                                                         _
 _       http://open-lab.com                                                                                                                        _
 _ blog: http://pupunzi.open-lab.com                                                                                                                _
 _ Q&A:  http://jquery.pupunzi.com                                                                                                                  _
 _                                                                                                                                                  _
 _ Licences: MIT, GPL                                                                                                                               _
 _    http://www.opensource.org/licenses/mit-license.php                                                                                            _
 _    http://www.gnu.org/licenses/gpl.html                                                                                                          _
 _                                                                                                                                                  _
 _ Copyright (c) 2001-2015. Matteo Bicocchi (Pupunzi);                                                                                              _
 ___________________________________________________________________________________________________________________________________________________*/

jQuery.mbBgndGallery.effects = {

	fade: {
		enter: {
			left: 0,
			opacity: 0
		},
		exit: {
			left: 0,
			opacity: 0
		},
		enterTiming: "ease-in",
		exitTiming: "ease-in"
	},

	slideUp: {
		enter: {
			top: "100%",
			opacity: 0
		},
		exit: {
			top: 0,
			opacity: 0
		},
		enterTiming: "ease-in",
		exitTiming: "ease-in"
	},

	slideDown: {
		enter: {
			top: "-100%",
			opacity: 0
		},
		exit: {
			top: 0,
			opacity: 0
		},
		enterTiming: "ease-in",
		exitTiming: "ease-in"
	},

	slideLeft: {
		enter: {
			x: "100%",
			opacity: 0
		},
		exit: {
			x: "-100%",
			opacity: 0
		},
		enterTiming: "easeOutQuad",
		exitTiming: "easeOutQuad"
	},

	slideRight: {
		enter: {
			x: "-100%",
			opacity: 1
		},
		exit: {
			y: "100%",
			opacity: 0
		}
	},

	zoom: {
		enter: {
			scale: ( 1 + Math.random() * 5 ),
			opacity: 0
		},
		exit: {
			scale: ( 1 + Math.random() * 5 ),
			opacity: 0
		},
		enterTiming: "cubic-bezier(0.19, 1, 0.22, 1)",
		exitTiming: "cubic-bezier(0.19, 1, 0.22, 1)"
	},

	zoomBlur: { //the blur effect only works on webkit browsers.
		enter: {
			opacity: 0,
			blur: 10,
			scale: 2
		},
		exit: {
			opacity: 0,
			blur: 10,
			scale: 2
		},
		enterTiming: "cubic-bezier(0.19, 1, 0.22, 1)",
		exitTiming: "cubic-bezier(0.19, 1, 0.22, 1)"
	},

	blur: { //the blur effect only works on webkit browsers.
		enter: {
			opacity: 0,
			blur: 10
		},
		exit: {
			opacity: 0,
			blur: 10
		},
		enterTiming: "cubic-bezier(0.19, 1, 0.22, 1)",
		exitTiming: "cubic-bezier(0.19, 1, 0.22, 1)"
	}

};
;
/*
 * ******************************************************************************
 *  jquery.mb.components
 *  file: jquery.mb.CSSAnimate.min.js
 *
 *  Copyright (c) 2001-2014. Matteo Bicocchi (Pupunzi);
 *  Open lab srl, Firenze - Italy
 *  email: matteo@open-lab.com
 *  site: 	http://pupunzi.com
 *  blog:	http://pupunzi.open-lab.com
 * 	http://open-lab.com
 *
 *  Licences: MIT, GPL
 *  http://www.opensource.org/licenses/mit-license.php
 *  http://www.gnu.org/licenses/gpl.html
 *
 *  last modified: 26/03/14 21.40
 *  *****************************************************************************
 */

jQuery.support.CSStransition=function(){var d=(document.body||document.documentElement).style;return void 0!==d.transition||void 0!==d.WebkitTransition||void 0!==d.MozTransition||void 0!==d.MsTransition||void 0!==d.OTransition}();function uncamel(d){return d.replace(/([A-Z])/g,function(a){return"-"+a.toLowerCase()})}function setUnit(d,a){return"string"!==typeof d||d.match(/^[\-0-9\.]+jQuery/)?""+d+a:d}
function setFilter(d,a,b){var c=uncamel(a),g=jQuery.browser.mozilla?"":jQuery.CSS.sfx;d[g+"filter"]=d[g+"filter"]||"";b=setUnit(b>jQuery.CSS.filters[a].max?jQuery.CSS.filters[a].max:b,jQuery.CSS.filters[a].unit);d[g+"filter"]+=c+"("+b+") ";delete d[a]}
jQuery.CSS={name:"mb.CSSAnimate",author:"Matteo Bicocchi",version:"2.0.0",transitionEnd:"transitionEnd",sfx:"",filters:{blur:{min:0,max:100,unit:"px"},brightness:{min:0,max:400,unit:"%"},contrast:{min:0,max:400,unit:"%"},grayscale:{min:0,max:100,unit:"%"},hueRotate:{min:0,max:360,unit:"deg"},invert:{min:0,max:100,unit:"%"},saturate:{min:0,max:400,unit:"%"},sepia:{min:0,max:100,unit:"%"}},normalizeCss:function(d){var a=jQuery.extend(!0,{},d);jQuery.browser.webkit||jQuery.browser.opera?jQuery.CSS.sfx=
		"-webkit-":jQuery.browser.mozilla?jQuery.CSS.sfx="-moz-":jQuery.browser.msie&&(jQuery.CSS.sfx="-ms-");jQuery.CSS.sfx="";for(var b in a){"transform"===b&&(a[jQuery.CSS.sfx+"transform"]=a[b],delete a[b]);"transform-origin"===b&&(a[jQuery.CSS.sfx+"transform-origin"]=d[b],delete a[b]);"filter"!==b||jQuery.browser.mozilla||(a[jQuery.CSS.sfx+"filter"]=d[b],delete a[b]);"blur"===b&&setFilter(a,"blur",d[b]);"brightness"===b&&setFilter(a,"brightness",d[b]);"contrast"===b&&setFilter(a,"contrast",d[b]);"grayscale"===
b&&setFilter(a,"grayscale",d[b]);"hueRotate"===b&&setFilter(a,"hueRotate",d[b]);"invert"===b&&setFilter(a,"invert",d[b]);"saturate"===b&&setFilter(a,"saturate",d[b]);"sepia"===b&&setFilter(a,"sepia",d[b]);if("x"===b){var c=jQuery.CSS.sfx+"transform";a[c]=a[c]||"";a[c]+=" translateX("+setUnit(d[b],"px")+")";delete a[b]}"y"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" translateY("+setUnit(d[b],"px")+")",delete a[b]);"z"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" translateZ("+
		setUnit(d[b],"px")+")",delete a[b]);"rotate"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" rotate("+setUnit(d[b],"deg")+")",delete a[b]);"rotateX"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" rotateX("+setUnit(d[b],"deg")+")",delete a[b]);"rotateY"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" rotateY("+setUnit(d[b],"deg")+")",delete a[b]);"rotateZ"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" rotateZ("+setUnit(d[b],"deg")+")",delete a[b]);"scale"===b&&
(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" scale("+setUnit(d[b],"")+")",delete a[b]);"scaleX"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" scaleX("+setUnit(d[b],"")+")",delete a[b]);"scaleY"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" scaleY("+setUnit(d[b],"")+")",delete a[b]);"scaleZ"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" scaleZ("+setUnit(d[b],"")+")",delete a[b]);"skew"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" skew("+setUnit(d[b],
		"deg")+")",delete a[b]);"skewX"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" skewX("+setUnit(d[b],"deg")+")",delete a[b]);"skewY"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" skewY("+setUnit(d[b],"deg")+")",delete a[b]);"perspective"===b&&(c=jQuery.CSS.sfx+"transform",a[c]=a[c]||"",a[c]+=" perspective("+setUnit(d[b],"px")+")",delete a[b])}return a},getProp:function(d){var a=[],b;for(b in d)0>a.indexOf(b)&&a.push(uncamel(b));return a.join(",")},animate:function(d,a,b,c,g){return this.each(function(){function n(){e.called=
		!0;e.CSSAIsRunning=!1;h.off(jQuery.CSS.transitionEnd+"."+e.id);clearTimeout(e.timeout);h.css(jQuery.CSS.sfx+"transition","");"function"==typeof g&&g.apply(e);"function"==typeof e.CSSqueue&&(e.CSSqueue(),e.CSSqueue=null)}var e=this,h=jQuery(this);e.id=e.id||"CSSA_"+(new Date).getTime();var k=k||{type:"noEvent"};if(e.CSSAIsRunning&&e.eventType==k.type&&!jQuery.browser.msie&&9>=jQuery.browser.version)e.CSSqueue=function(){h.CSSAnimate(d,a,b,c,g)};else if(e.CSSqueue=null,e.eventType=k.type,0!==h.length&&
		d){d=jQuery.normalizeCss(d);e.CSSAIsRunning=!0;"function"==typeof a&&(g=a,a=jQuery.fx.speeds._default);"function"==typeof b&&(c=b,b=0);"string"==typeof b&&(g=b,b=0);"function"==typeof c&&(g=c,c="cubic-bezier(0.65,0.03,0.36,0.72)");if("string"==typeof a)for(var l in jQuery.fx.speeds)if(a==l){a=jQuery.fx.speeds[l];break}else a=jQuery.fx.speeds._default;a||(a=jQuery.fx.speeds._default);"string"===typeof g&&(c=g,g=null);if(jQuery.support.CSStransition){var f={"default":"ease","in":"ease-in",out:"ease-out",
	"in-out":"ease-in-out",snap:"cubic-bezier(0,1,.5,1)",easeOutCubic:"cubic-bezier(.215,.61,.355,1)",easeInOutCubic:"cubic-bezier(.645,.045,.355,1)",easeInCirc:"cubic-bezier(.6,.04,.98,.335)",easeOutCirc:"cubic-bezier(.075,.82,.165,1)",easeInOutCirc:"cubic-bezier(.785,.135,.15,.86)",easeInExpo:"cubic-bezier(.95,.05,.795,.035)",easeOutExpo:"cubic-bezier(.19,1,.22,1)",easeInOutExpo:"cubic-bezier(1,0,0,1)",easeInQuad:"cubic-bezier(.55,.085,.68,.53)",easeOutQuad:"cubic-bezier(.25,.46,.45,.94)",easeInOutQuad:"cubic-bezier(.455,.03,.515,.955)",
	easeInQuart:"cubic-bezier(.895,.03,.685,.22)",easeOutQuart:"cubic-bezier(.165,.84,.44,1)",easeInOutQuart:"cubic-bezier(.77,0,.175,1)",easeInQuint:"cubic-bezier(.755,.05,.855,.06)",easeOutQuint:"cubic-bezier(.23,1,.32,1)",easeInOutQuint:"cubic-bezier(.86,0,.07,1)",easeInSine:"cubic-bezier(.47,0,.745,.715)",easeOutSine:"cubic-bezier(.39,.575,.565,1)",easeInOutSine:"cubic-bezier(.445,.05,.55,.95)",easeInBack:"cubic-bezier(.6,-.28,.735,.045)",easeOutBack:"cubic-bezier(.175, .885,.32,1.275)",easeInOutBack:"cubic-bezier(.68,-.55,.265,1.55)"};
	f[c]&&(c=f[c]);h.off(jQuery.CSS.transitionEnd+"."+e.id);f=jQuery.CSS.getProp(d);var m={};jQuery.extend(m,d);m[jQuery.CSS.sfx+"transition-property"]=f;m[jQuery.CSS.sfx+"transition-duration"]=a+"ms";m[jQuery.CSS.sfx+"transition-delay"]=b+"ms";m[jQuery.CSS.sfx+"transition-timing-function"]=c;setTimeout(function(){h.one(jQuery.CSS.transitionEnd+"."+e.id,n);h.css(m)},1);e.timeout=setTimeout(function(){e.called||!g?(e.called=!1,e.CSSAIsRunning=!1):(h.css(jQuery.CSS.sfx+"transition",""),g.apply(e),e.CSSAIsRunning=
			!1,"function"==typeof e.CSSqueue&&(e.CSSqueue(),e.CSSqueue=null))},a+b+10)}else{for(f in d)"transform"===f&&delete d[f],"filter"===f&&delete d[f],"transform-origin"===f&&delete d[f],"auto"===d[f]&&delete d[f],"x"===f&&(k=d[f],l="left",d[l]=k,delete d[f]),"y"===f&&(k=d[f],l="top",d[l]=k,delete d[f]),"-ms-transform"!==f&&"-ms-filter"!==f||delete d[f];h.delay(b).animate(d,a,g)}}})}};jQuery.fn.CSSAnimate=jQuery.CSS.animate;jQuery.normalizeCss=jQuery.CSS.normalizeCss;
jQuery.fn.css3=function(d){return this.each(function(){var a=jQuery(this),b=jQuery.normalizeCss(d);a.css(b)})};
;/*
 * ******************************************************************************
 *  jquery.mb.components
 *  file: jquery.mb.browser.min.js
 *
 *  Copyright (c) 2001-2014. Matteo Bicocchi (Pupunzi);
 *  Open lab srl, Firenze - Italy
 *  email: matteo@open-lab.com
 *  site: 	http://pupunzi.com
 *  blog:	http://pupunzi.open-lab.com
 * 	http://open-lab.com
 *
 *  Licences: MIT, GPL
 *  http://www.opensource.org/licenses/mit-license.php
 *  http://www.gnu.org/licenses/gpl.html
 *
 *  last modified: 26/03/14 21.43
 *  *****************************************************************************
 */

var nAgt=navigator.userAgent;if(!jQuery.browser){jQuery.browser={},jQuery.browser.mozilla=!1,jQuery.browser.webkit=!1,jQuery.browser.opera=!1,jQuery.browser.safari=!1,jQuery.browser.chrome=!1,jQuery.browser.androidStock=!1,jQuery.browser.msie=!1,jQuery.browser.ua=nAgt,jQuery.browser.name=navigator.appName,jQuery.browser.fullVersion=""+parseFloat(navigator.appVersion),jQuery.browser.majorVersion=parseInt(navigator.appVersion,10);var nameOffset,verOffset,ix;if(-1!=(verOffset=nAgt.indexOf("Opera")))jQuery.browser.opera=!0,jQuery.browser.name="Opera",jQuery.browser.fullVersion=nAgt.substring(verOffset+6),-1!=(verOffset=nAgt.indexOf("Version"))&&(jQuery.browser.fullVersion=nAgt.substring(verOffset+8));else if(-1!=(verOffset=nAgt.indexOf("OPR")))jQuery.browser.opera=!0,jQuery.browser.name="Opera",jQuery.browser.fullVersion=nAgt.substring(verOffset+4);else if(-1!=(verOffset=nAgt.indexOf("MSIE")))jQuery.browser.msie=!0,jQuery.browser.name="Microsoft Internet Explorer",jQuery.browser.fullVersion=nAgt.substring(verOffset+5);else if(-1!=nAgt.indexOf("Trident")||-1!=nAgt.indexOf("Edge")){jQuery.browser.msie=!0,jQuery.browser.name="Microsoft Internet Explorer";var start=nAgt.indexOf("rv:")+3,end=start+4;jQuery.browser.fullVersion=nAgt.substring(start,end)}else-1!=(verOffset=nAgt.indexOf("Chrome"))?(jQuery.browser.webkit=!0,jQuery.browser.chrome=!0,jQuery.browser.name="Chrome",jQuery.browser.fullVersion=nAgt.substring(verOffset+7)):nAgt.indexOf("mozilla/5.0")>-1&&nAgt.indexOf("android ")>-1&&nAgt.indexOf("applewebkit")>-1&&!(nAgt.indexOf("chrome")>-1)?(verOffset=nAgt.indexOf("Chrome"),jQuery.browser.webkit=!0,jQuery.browser.androidStock=!0,jQuery.browser.name="androidStock",jQuery.browser.fullVersion=nAgt.substring(verOffset+7)):-1!=(verOffset=nAgt.indexOf("Safari"))?(jQuery.browser.webkit=!0,jQuery.browser.safari=!0,jQuery.browser.name="Safari",jQuery.browser.fullVersion=nAgt.substring(verOffset+7),-1!=(verOffset=nAgt.indexOf("Version"))&&(jQuery.browser.fullVersion=nAgt.substring(verOffset+8))):-1!=(verOffset=nAgt.indexOf("AppleWebkit"))?(jQuery.browser.webkit=!0,jQuery.browser.safari=!0,jQuery.browser.name="Safari",jQuery.browser.fullVersion=nAgt.substring(verOffset+7),-1!=(verOffset=nAgt.indexOf("Version"))&&(jQuery.browser.fullVersion=nAgt.substring(verOffset+8))):-1!=(verOffset=nAgt.indexOf("Firefox"))?(jQuery.browser.mozilla=!0,jQuery.browser.name="Firefox",jQuery.browser.fullVersion=nAgt.substring(verOffset+8)):(nameOffset=nAgt.lastIndexOf(" ")+1)<(verOffset=nAgt.lastIndexOf("/"))&&(jQuery.browser.name=nAgt.substring(nameOffset,verOffset),jQuery.browser.fullVersion=nAgt.substring(verOffset+1),jQuery.browser.name.toLowerCase()==jQuery.browser.name.toUpperCase()&&(jQuery.browser.name=navigator.appName));-1!=(ix=jQuery.browser.fullVersion.indexOf(";"))&&(jQuery.browser.fullVersion=jQuery.browser.fullVersion.substring(0,ix)),-1!=(ix=jQuery.browser.fullVersion.indexOf(" "))&&(jQuery.browser.fullVersion=jQuery.browser.fullVersion.substring(0,ix)),jQuery.browser.majorVersion=parseInt(""+jQuery.browser.fullVersion,10),isNaN(jQuery.browser.majorVersion)&&(jQuery.browser.fullVersion=""+parseFloat(navigator.appVersion),jQuery.browser.majorVersion=parseInt(navigator.appVersion,10)),jQuery.browser.version=jQuery.browser.majorVersion}jQuery.browser.android=/Android/i.test(nAgt),jQuery.browser.blackberry=/BlackBerry|BB|PlayBook/i.test(nAgt),jQuery.browser.ios=/iPhone|iPad|iPod|webOS/i.test(nAgt),jQuery.browser.operaMobile=/Opera Mini/i.test(nAgt),jQuery.browser.windowsMobile=/IEMobile|Windows Phone/i.test(nAgt),jQuery.browser.kindle=/Kindle|Silk/i.test(nAgt),jQuery.browser.mobile=jQuery.browser.android||jQuery.browser.blackberry||jQuery.browser.ios||jQuery.browser.windowsMobile||jQuery.browser.operaMobile||jQuery.browser.kindle,jQuery.isMobile=jQuery.browser.mobile,jQuery.isTablet=jQuery.browser.mobile&&jQuery(window).width()>765,jQuery.isAndroidDefault=jQuery.browser.android&&!/chrome/i.test(nAgt);
