$(document).ready(function () {
  const api = new API()

  // Hide / show left panel
  $(document).on("click", ".context_menu_button", function() { api.adjust_panels() });

  // Dropdown menu
  $(document).on("click", ".dropdown", function() { api.toggle_menu(this) })

  // Textarea resize
  $(document).on('input', '.label_field, .content_field', function () { api.resizeTextareas(this) });
  



  // Create file
  $(document).on("click", ".create_button", function() { api.files.start_creating() });

  // Delete file
  $(document).on("click", ".delete-button", function() { api.files.start_deleting(this) });
  

  // Open file
  $(document).on("click", ".file_button, .tab_button", function() { api.files.open(this) });
  
  // Close file
  $(document).on("click", ".close-button", function() { api.files.close(this) });
  
  // Save file
  $(document).on("click", ".save-button", function() { api.files.save(this) })
});
