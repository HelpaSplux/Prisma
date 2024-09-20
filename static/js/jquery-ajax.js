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
  if(!$target.closest('.file-creation-form').length && !$(".file-creation-form").css("top").includes("-")) {
      $(".file-creation-form").animate({top: "-40%"});
      $(".file-name-input").blur(); 
  }        
  });


  // Sends ajax query when file creation form submited and hide form after
  $("form#id-file-creation-form").submit(function(e) {
    var url = $(this).attr("action");
    var label = $(".file-name-input").val()
    var file_button_id = label.replaceAll(" ", "_") + "_button_id";

    $.ajax({
      type: "POST",
      url: url,
      data: {
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        'label': label,
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
        var button = `<button class="file_button" id="${file_button_id}" type="button">${label}</button>` 
        $(".file_list").append(button);
        $(".file_list").animate({scrollTop: $("#" + file_button_id).offset().top});
        $("#" + file_button_id).addClass("file_button_active");
        setTimeout(() => {
          $("#" + file_button_id).removeClass("file_button_active");
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

  // Send get request to obtain file data and show it to user
  $(document).on("click", ".file_button, .tab_button", function(event) {
    var file_label = $(event.target).text();

    var replaced_label = file_label.replaceAll(" ", "_");
    var panel_id = replaced_label + "_panel_id";
    var tab_id = replaced_label + "_tab_id";
    var file_button_id = replaced_label + "_button_id";

    if (!$("#" + panel_id).length) {
      $.get($(".file_list").attr("href"), {label: file_label}, function(data, status) {
        if (status == "success") {

          // Hides all panels.
          // Added new panel.
          // Shows current (new) panel.
          $(".bottom_right_panel").fadeOut(100);
          setTimeout(function () {
            $(".content").append(data);
          },100);
          setTimeout(function () {
            $("#" + panel_id).fadeIn(100);
          },100);
          
          // Added tab.
          // Makes inactive other tabs.
          // Makes new tab active.
          // Shows current tab.
          setTimeout(function () {
            $(".tab_bar").append(`<button id="${tab_id}" class="tab_button" type="button">${file_label}</button>`);
            $(".tab_button").removeClass("tab_button_active");
            $(`#${tab_id}`).addClass("tab_button_active");
          }, 100);
          setTimeout(function () {
            $(`#${tab_id}`).fadeIn(100)
          }, 100);

          // Makes inative all file buttons.
          // Makes active current button.
          $(".file_button").removeClass("file_button_active");
          $(`#${file_button_id}`).toggleClass("file_button_active");


        }    
        
      });
    } else {
      
      // Hides all panels
      // Shows current panel
      $(".bottom_right_panel").fadeOut(100);
      setTimeout(function () {
        $("#" + panel_id).fadeIn(100);
      },100);

      // Shows tab
      var removed_tab = $(`#${tab_id}`)[0]
      if ($(`#${tab_id}`).css("display") == "none") {
        setTimeout(function () {
          removed_tab.remove()
          $(".tab_bar").append($(removed_tab))
          $(`#${tab_id}`).fadeIn(100)
        }, 100);

      }

      // Makes inactive all file buttons.
      // Makes active current button.
      // Scroll to active button.
      $(".file_button").removeClass("file_button_active");
      $(`#${file_button_id}`).toggleClass("file_button_active");
      $(".file_list").animate({scrollTop: ($(".file_list").scrollTop() + $("#" + file_button_id).position().top) - 40});

      // Make inactive other tabs.
      // Make new tab active.
      $(".tab_button").removeClass("tab_button_active");
      $(`#${tab_id}`).addClass("tab_button_active");
    };


  });

  // Automatically change label field's height to fit the content inside
  $(document).on('input', '.label_field, .content_field', function () {
    var step = $(this).css("min-height").replace("px", "")
    var scroll_height = $(this).prop("scrollHeight")
    var style_height = $(this).css("height").replace("px","")
    
    if (scroll_height > style_height) {
      $(this).css("height", `${scroll_height}px`)

    }
    
    while (scroll_height == style_height && style_height > 32) {
      $(this).css("height", `${+style_height - +step}px`);
      style_height = $(this).css("height").replace("px","")
      scroll_height = $(this).prop("scrollHeight")

      if (scroll_height > style_height) {
        
        $(this).css("height", `${+style_height + +step}px`);
        break

      }

    }
    
  });

  // Makes invisible tab, right panel
  // Makes inactive file button on the left panel
  $(document).on("click", ".close_file_button", function() {
    $(".bottom_right_panel").fadeOut(100);
    $(".tab_button_active").fadeOut(100);

    let all_tabs = $(".tab_button")
    let visible_tabs = []
    
    for (var tab = 0; tab < all_tabs.length; tab++) {
      var current_tab = all_tabs[tab]
      if ($(current_tab).css("display") != "none") {
        visible_tabs.push(current_tab);
      }}
    
    let active_tab = $(".tab_button_active")
    let button_index = $(visible_tabs).index(active_tab)
    
    
    $(".file_button").removeClass("file_button_active");
    if (visible_tabs.length > 1) {
      if (button_index > 0) {
        button_index -= 1
      } else {
        button_index += 1
      } 

      visible_tabs[button_index].click()
    }
  })

  
});
