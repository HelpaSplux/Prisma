
// Play hide/show animation for context menu button (on the top left)
$( ".context_menu_button" ).click(function(event) {
    event.preventDefault();
    if ($( "#left-panel" ).css("left") == "0px") {

      $(".bottom_left_panel").animate({"left": "-=250px"});
      $(".bottom_right_panel").animate({"width": "+=250px"});

    } else {

      $(".bottom_left_panel").animate({"left": "+=250px"});
      $(".bottom_right_panel").animate({"width": "-=250px"});

    };
  });


// Play show/hide animation for file creation form on pressing "+" button
$(".create_button").click(function () {
if ($(".file-creation-form").css("top").includes("-")) {
    
    $(".file-creation-form").animate({top: "40%"});
    setTimeout(() => {
    $(".file-name-input").focus();
    }, 500);
    
} else {

    $(".file-creation-form").animate({top: "-40%"});
    $(".file-name-input").blur();  

}
});


// Play hide animation for the file creation form on click outside of this element 
$(document).click(function(event) { 
var $target = $(event.target);
console.log($target)
if(!$target.closest('.file-creation-form').length && !$(".file-creation-form").css("top").includes("-")) {
    $(".file-creation-form").animate({top: "-40%"});
    $(".file-name-input").blur(); 
}        
});
