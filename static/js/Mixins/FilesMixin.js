const FilesMixin = {
    collect_files() {
        const buttons = this.panels.left.buttons.all
        const files = new Map()

        for (const [id, button] of buttons) {
            let file = new File(button)
            files.set(file.id, file)
        }

        return files
    },

    open_next_file() {
        const next_file = this.get_next_file()
        if (!next_file) {return}
        
        this.open_file(next_file)
        return
    },

    get_next_file() {
        let opened_files = this.files.opened

        // Opened less then 1 file
        if (opened_files.length <= 1) return

        let active_index = opened_files.indexOf(this.files.active)
        let next_index
        
        // Calculate next file index
        if (active_index == 0) {
            next_index = active_index + 1
        }
        else if (active_index > 0) {
            next_index = active_index - 1
        }
        
        // Get next file
        let next_id = opened_files[next_index]
        let next_file = this.files.all.get(next_id)
        return next_file
    },
}