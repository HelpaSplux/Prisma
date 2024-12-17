class File {
    buttons = {}
    panel

    constructor(button) {
        this.id = button.id
        this._name = button.name
        this.buttons.left = button
    }


    get menu() {return this.panel.menu}

    get url() {return this.panel.url}
    
    get token() {return this.panel.csrf_token}
    
    get name() {return this._name}
    
    get new_name() {return this.panel.label.val()}
    
    get content() {return this.panel.content.text()}
    
    get new_content() {return this.panel.content.val()}




    set name(new_name) {
        this.buttons.top.name = new_name
        this.buttons.left.name = new_name
        this._name = new_name
    }

    set content(new_content) {
        this.panel.content.text(new_content)
    }



    resizeTextareas() {this.panel.resizeTextareas()}


    is_opened() {
        const state = this._state
        if (state == "closed") return false

        return true
    }


    close() {
        this.buttons.left.deactivate()
        this.buttons.top.deactivate()
        this.buttons.top.hide()
        this.panel.hide()
        this._state = "closed"
    }

    open() {
        this.buttons.left.activate()
        this.buttons.top.activate()
        this.buttons.top.show()
        this.panel.show()
        this._state = "opened"
    }

    hide() {
        this.buttons.left.deactivate()
        this.buttons.top.deactivate()
        this.panel.hide()
        this._state = "hidden"
    }
}

