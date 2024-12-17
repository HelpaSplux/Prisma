const SaveFileMixin = {
    save_file(object) {
        const files = this.files.all
        const id = this.get_id(object)
        const file = files.get(id)

        const file_changed = this.is_changed(file)
        if (!file_changed) return 

        const response = this.post(file)
        
        response
        .always((data) => {new Notification(data)})
        .done(() => {this.change_file(file)})

        file.menu.deactivate()
    },

    change_file(file) {
        const name = file.new_name
        const content = file.new_content

        file.name = name
        file.content = content
        return
    },

    is_changed(file) {
        const name = {
            old: file.name,
            new: file.new_name,
            get changed() {return this.old != this.new}
        }
        const content = {
            old: file.content,
            new: file.new_content,
            get changed() {return this.old != this.new}
        }

        const file_changed = name.changed || content.changed

        if(file_changed) return true

        const data = {"message": "There's nothing to save."}     
        new Notification(data)

        return false
    },

    post(file) {
        const url = file.url
        const data = {
            'csrfmiddlewaretoken': file.token,
            'old_label': file.name,
            'new_label': file.new_name,
            'content': file.new_content
        }

        const response = $.post({url: url, data: data});

        return response
    }
}