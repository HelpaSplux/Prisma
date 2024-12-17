const CreateFileMixin = {
    start_creating() {
        const form = this.forms.creation
        form.prepare()
        form.show()

        form.input.done(() => { form.post() })
        form.request
        .done(() => { this.create_file(form.title) })
        .always(() => {
            form.hide()
            this.check_for_duplicate(form)
            new Notification(form.response)
        })
    },

    create_file(title) {
        let button = this.panels.left.buttons.create(title)
            
        let file = new File(button)
        this.files.all.set(file.id, file)
        return
    },

    check_for_duplicate(form) {
        const duplicate = form.duplicate
        if (duplicate) { this.show_duplicate(duplicate) }
        return
    },
    
    show_duplicate(duplicate) {
        let duplicate_file = this.files.all.get(duplicate)
        let button = duplicate_file.buttons.left

        this.panels.left.scroll_to(button)
        button.highlight()
        return
    },
}