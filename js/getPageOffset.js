/**
 * @function function() returns the window.pageYOffset of the webpage, we need that so we can keep on scrolling until the page
 * offset becomes constant.
 *
 * @return {Number} window.pageYOffset.
 */

(function () {
  return window.pageYOffset !== undefined
    ? window.pageYOffset
    : document.documentElement || document.body.parentNode || document.body;
})();
