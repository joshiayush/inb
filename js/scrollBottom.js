/**
 * @function function() scrolls the web page to the very bottom of it using the 'document.scrollingElement.scrollTop' property.
 */

(function () {
  var scrollingElement = document.scrollingElement || document.body;
  scrollingElement.scrollTop = scrollingElement.scrollHeight;
})();
