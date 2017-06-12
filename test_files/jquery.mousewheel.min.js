/* Copyright (c) 2011 Brandon Aaron (http://brandonaaron.net)
 * Licensed under the MIT License (LICENSE.txt).
 *
 * Thanks to: http://adomas.org/javascript-mouse-wheel/ for some pointers.
 * Thanks to: Mathias Bank(http://www.mathias-bank.de) for a scope bug fix.
 * Thanks to: Seamus Leahy for adding deltaX and deltaY
 *
 * Version: 3.0.6
 * 
 * Requires: 1.2.2+
 */
(function(b){var c=["DOMMouseScroll","mousewheel"];if(b.event.fixHooks){for(var d=c.length;d;){b.event.fixHooks[c[--d]]=b.event.mouseHooks}}b.event.special.mousewheel={setup:function(){if(this.addEventListener){for(var e=c.length;e;){this.addEventListener(c[--e],a,false)}}else{this.onmousewheel=a}},teardown:function(){if(this.removeEventListener){for(var e=c.length;e;){this.removeEventListener(c[--e],a,false)}}else{this.onmousewheel=null}}};b.fn.extend({mousewheel:function(e){return e?this.bind("mousewheel",e):this.trigger("mousewheel")},unmousewheel:function(e){return this.unbind("mousewheel",e)}});function a(h){var g=h||window.event,f=[].slice.call(arguments,1),i=0,e=true,k=0,j=0;h=b.event.fix(g);h.type="mousewheel";if(g.wheelDelta){i=g.wheelDelta/120}if(g.detail){i=-g.detail/3}j=i;if(g.axis!==undefined&&g.axis===g.HORIZONTAL_AXIS){j=0;k=-1*i}if(g.wheelDeltaY!==undefined){j=g.wheelDeltaY/120}if(g.wheelDeltaX!==undefined){k=-1*g.wheelDeltaX/120}f.unshift(h,i,k,j);return(b.event.dispatch||b.event.handle).apply(this,f)}})(jQuery);