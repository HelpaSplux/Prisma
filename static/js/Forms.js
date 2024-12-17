class Form {
    constructor(fields) {
        this.id = fields.id
        this.classes = fields.classes
        this.objects = this.configure_objects()
    }



    configure_objects() {
        const objects = {
            self: $(`.${this.classes.self}`),
        }
        return objects
    }
    prepare() {
        this.request = $.Deferred()
        this.input = $.Deferred()
    }



    toggle() {
        const active = this.is_active()

        if (active) {
            this.hide()
        }
        else if (!active) {
            this.show()
        }
    }
    show() {
        this.objects.self.addClass(this.classes.toggle)
        this.add_listeners()
    }
    hide() {
        this.objects.self.removeClass(this.classes.toggle)
        this.remove_listeners()
    }



    is_active() {
        let element_class = this.objects.self.attr("class")
        let status = element_class.includes(this.classes.toggle)

        return status
    }



    add_listeners() {
        $(document).on("click.creation_form", "body", this.hide_on_click.bind(this))
    }
    remove_listeners() {
        $(document).off("click.creation_form")
    }

    hide_on_click(event) {
        let target = $(event.target)

        let click_in_form = target.closest(this.objects.self).length
        if (!click_in_form) {
            this.hide()
        }   
        return target
    }

    process_response(response) {
        response    
        .always((response) => { this.response = response })
        .done(() => {this.request.resolve()})
        .fail(() => {this.request.reject()})
        return
    }
}   



class CreationForm extends Form {
    messages = {
        blank: "Title field can't be blank.",
        duplicate: "This file already exists.",
    }

    constructor(fields, files) {
        super(fields)
        this.files = files
        this._duplicate = null
        this.url = this.objects.form.attr("action")
        this.csrf_token = $("input[name=csrfmiddlewaretoken]").val()
    }

    get duplicate() {
        let result = this._duplicate
        this._duplicate = null
        return result
    }


    configure_objects() {
        const objects = super.configure_objects()
        objects.form = objects.self.find(`#${this.id.form}`)
        objects.submit_button = $(`#${this.id.submit_button}`)
        objects.input_field = $(`.${this.classes.input_field}`)

        return objects
    }
    prepare() {
        super.prepare()
        this.objects.input_field.val("")
    }



    show() {
        super.show()
        setTimeout(() => { this.objects.input_field.focus() }, 500);
    }
    hide() {
        super.hide()
        this.objects.input_field.blur();  
    }



    add_listeners() {
        super.add_listeners()
        $(document).on("click.submit", `#${this.id.submit_button}`, this.process_input.bind(this))
    }
    remove_listeners() {
        setTimeout(super.remove_listeners, 0)
        $(document).off("click.submit")
    }


    process_input(event) {
        event.preventDefault()

        const title = this.objects.input_field.val() 
        const title_valid = this.validate(title)

        if (!title_valid) {
            this.response =  this.prepare_message()

            this.request.reject()
            this.input.reject()
            return
        }   

        // Title valid
        this.title = title
        this.input.resolve()
        return
    }


    validate(title) {
        if (!title) {return false}

        // Duplicate
        for (const [id, file] of this.files.all) {
            if (file.name == title) {
                this._duplicate = id
                return false
            }
        }
        return true
    }
    
    prepare_message() {
        const message = this.messages.blank
        if (this._duplicate) {
            message = this.messages.duplicate
        }
        return {"message": message}
    }

    post() {
        const data = {
            'csrfmiddlewaretoken': this.csrf_token,
            'label': this.title,    
        }
        const response = $.post({ url: this.url, data: data })
        this.process_response(response)
        
        return false
    }
}




class DeletionForm extends Form {
    constructor(fields) {
        super(fields)
        this.url = this.objects.self.attr("href")
    }
    

    configure_objects() {
        const objects = super.configure_objects()
        objects.message_field = $(`.${this.classes.message_field}`)
        objects.buttons = {
            submit: $(`#${this.id.buttons.submit}`),
            cancel: $(`#${this.id.buttons.cancel}`),
        }

        return objects
    }

    prepare(file_name) {
        super.prepare()
        this.file_name = file_name

        let message = `Are you sure you want to delete "${file_name}"?`
        this.objects.message_field.html(message)
    }

    hide_on_click(event) {
        const target = super.hide_on_click(event)
        const click_on_close = target.attr("id") == this.id.buttons.cancel
        
        if (click_on_close) { 
            this.hide() 
        }
        return
    }
    
    add_listeners() {
        super.add_listeners()
        $(document).on("click", `#${this.id.buttons.submit}`, this.process_input.bind(this))
    }
    
    process_input(event) {
        event.preventDefault()

        this.input.resolve()

        return
    }

    get() {
        const url = this.url
        const parametrs = {label: this.file_name}

        const response = $.get(url, parametrs)        
        this.process_response(response)
    }
}



class FileCreationForm extends CreationForm {
    constructor(files) {
        const fields = {
            classes: {
                self: "file-creation-form",
                toggle: "active",
                input_field: "file-name-input",
            },
            id: {
                form: "id-file-creation-form",
                submit_button: "file-creation-form-submit" 
            }
        }
        super(fields, files)
        
    }
    

    // get title() {
    //     let title = this.objects.input_field.val() 
    //     return title
    // }
}   

class FileDeletionForm extends DeletionForm {
    constructor() {
        let fields = {
            classes: {
                self: "file-deletion-form",
                toggle: "active",
                message_field: "deletion-confirmation-message",
            },
            id: {
                buttons: {
                    submit: "file-deletion-form-delete",
                    cancel: "file-deletion-form-cancel",
                }
            }
        }
        super(fields)
    }
}

