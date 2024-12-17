const PanelsMixin = {
    adjust_panels() {
        // Left panel
        this.panels.left.toggle()

        // Right panel
        this.toggle_right_panels()
    },

    toggle_right_panels() {
        const active = this.files.active
        const files = this.files.all
        const file = files.get(active)

        if (!file) return

        const base_panel_class = file.panel.classes.self
        const panels = $("." + base_panel_class)
        const panel_fullscreen = panels.attr("class").includes("fullscreen")


        // Change class
        if (panel_fullscreen) { return panels.removeClass("fullscreen") } 

        if (!panel_fullscreen) { return panels.addClass("fullscreen") }


        throw new Error("Fail to toggle panels.")
    },

    repush_top_button(file) {
        if (file.is_opened()) return
        
        const button = file.buttons.top
        const panel = this.panels.top
        panel.move_button(button)

        return
    },

    resizeTextareas(object) {
        const id = this.get_id(object)
        const files = this.files.all
        const file = files.get(id)

        file.resizeTextareas()

        return
    },

    get_panel(file) {
        const url = this.panels.left.url
        const parametrs = {label: file.name, file_id: file.id}
        
        const request = 
        $.get(url, parametrs, (data, status) => {
            if (status == "success") { 
                let panel = new RightPanel(data, file.id)
                file.panel = panel
            }
        })
        return request
    },

    get_top_button(file) {
        const button = this.panels.top.add_button(file.name, file.id)
        file.buttons.top = button
        return
    }
}