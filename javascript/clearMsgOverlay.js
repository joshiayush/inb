/**
 * @function function() sets the display of the message overlay which we have on the page to none.
 * 
 * We need these type of functions in future too because we don't want any kind of interrupt while using the bot. 
 */

(function () {
    document.querySelector("div[class^='msg-overlay-list-bubble']").style = 'display: none';
})();