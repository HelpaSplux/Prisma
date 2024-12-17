const OpenFileMixin = {
    open_file(object) {
        const id = this.get_id(object)
        
        this.hide_active_file()

        // Open file
        const file = this.files.all.get(id)
        this.configure(file).done(() => { 
            this.repush_top_button(file)
            file.open()
        })

        // Show left button to user 
        this.panels.left.scroll_to(file.buttons.left)

        // Internal logic
        this.update_files(id)
        return
    },

    hide_active_file() {
        // Empty opened files
        const opened_files = this.files.opened.length
        if (opened_files == 0) return
        
        // Active is undefined
        const id = this.files.active
        if (!id) return

        // Hide file
        const file = this.files.all.get(id)
        file.hide()
        return
    },

    configure(file) {
        let deferred = $.Deferred()

        if (!file) {return deferred.reject()}

        // Create top button
        if (!file.buttons.top) { this.get_top_button(file) }

        // Create panel
        if (!file.panel) { return this.get_panel(file) }

        return deferred.resolve()
    },

    update_files(id) {
        // Active file
        const active_file = this.files.active
        if (active_file != id) {
            this.files.active = id

            if (this.files.active != id) throw new Error("Fail to update active file.")
        }

        // Opened files
        const opened_files = this.files.opened
        if (!(opened_files.includes(id))) {
            this.files.opened.push(id)
            if (!this.files.opened.includes(id)) throw new Error("Fail to update opened files.")
        }
        return
    },

    
}