$(document).ready(function () {
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


  // Sends ajax query when file creation form submited and hide form
  $("form#id-file-creation-form").submit(function(e) {
    var url = $(this).attr("action");

    $.ajax({
      type: "POST",
      url: url,
      data: {
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        'label': $(".file-name-input").val(),
      },
      success: function(data) {
        // Shows creation form
        $(".file-creation-form").animate({top: "-40%"});
        $(".file-name-input").blur(); 

        // Fill success_message_id element with message
        // and shows this message
        $("#success_message_id").html(data.message);
        $("#success_message_id").animate({bottom: "20px"});

        // Add file button to the list
        // scroll to it and highlits it
        $(".file_list").append(data.new_file);
        $(".file_list").animate({scrollTop: $(data.label_id).offset().top});
        $(data.label_id).addClass("file_button_active");
        setTimeout(() => {
          $(data.label_id).removeClass("file_button_active");
        }, 1500);

        // Hides message
        setTimeout(() => {
          $("#success_message_id").animate({bottom: "-50px"});
        }, 3000);
      },
      error: function(data) {
        // Fill error_message_id element with message
        // and shows this message      
        $("#error_message_id").html(data.responseJSON.message);
        $("#error_message_id").animate({bottom: "20px"});

        // Hides message
        setTimeout(() => {
          $("#error_message_id").animate({bottom: "-50px"});
        }, 3000);
      }
    });
    return false
  });


  $(document).on("click", ".file_button", function(event) {
    var file_label = $(event.target).text();
    var element = file_label + "_panel_id"
    element = element.replace(" ", "_")   
    console.log(element)

    if (!$("#" + element).length) {
      $.get($(".file_list").attr("href"), {label: file_label}, function(data, status) {
        if (status == "success") {
          $(".bottom_right_panel").fadeOut(100);
          setTimeout(function () {
            $(".content").append(data);
            console.log(element)
            $("#panel_id").attr("id", element);
          },100);


          setTimeout(function () {
            $("#" + element).fadeIn(100);
          },100);
          console.log($("#" + element));
  
          $(".file_button").removeClass("file_button_active");
          $(event.target).toggleClass("file_button_active");
          
        }    
        
      });
    } else {
      $(".bottom_right_panel").fadeOut(100);
      setTimeout(function () {
        $("#" + element).fadeIn(100);
      },100);

      $(".file_button").removeClass("file_button_active");
      $(event.target).toggleClass("file_button_active");
    };
  });

});