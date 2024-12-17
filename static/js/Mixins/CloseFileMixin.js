const CloseFileMixin = {
    close_file(object) {
        const panel = $(object).parent()
        const id = panel.attr("file-id")
        if (!id) {return}

        this.open_next_file()
        
        // Object's file
        const file = this.files.all.get(id)
        this.remove_from_opened(file)
        file.close()
    },

    remove_from_opened(file) {
        const opened_files = this.files.opened
        const file_index = opened_files.indexOf(file.id)

        if (file_index < 0) {return}
        
        opened_files.splice(file_index, 1)
        
        if (opened_files.includes(file.id)) throw new Error("File still in opened files.")
        return
    },
}