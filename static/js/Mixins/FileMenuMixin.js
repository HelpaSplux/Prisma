const FileMenuMixin = {
    toggle_menu(object) {
        const id = this.get_id(object)
        const file = this.files.all.get(id)

        if (!file) throw new Error("Fail to toggle menu.")

        file.menu.togle()
    },

    close_menu(id) {
        let file = this.files.get(id)
        file.menu.deactivate()
    },
}