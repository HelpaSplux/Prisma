const DeleteFileMixin = {
    start_deleting(object) {
        const id = this.get_id(object)
        const file = this.files.all.get(id)
        const form = this.forms.deletion

        form.prepare(file.name)
        form.show()

        form.input.done(() => { form.get() })
        form.request
        .done(() => { 
            this.open_next_file()
            this.delete_file(file) 
        })
        .always(() => {
            new Notification(form.response)
            form.hide()
        })
        

    },
    

    remove_file_components(file) {
        const panel = {
            top: this.panels.top,
            left: this.panels.left,
            right: file.panel,
        }

        panel.top.remove(file.id)
        panel.left.remove(file.id)
        panel.right.remove()

        return
    },

    delete_file(file) {
        this.remove_file_components(file)

        this.remove_from_files(file)
    },

    remove_from_files(file) {
        const all = this.files.all
        const opened = this.files.opened
        
        const id = file.id
        const index = opened.indexOf(id)

        opened.splice(index, 1)    
        all.delete(file.id)

        return
    }
}