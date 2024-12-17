const IdMixin = {
    
    get_id(object) {
        if (!object) {return}

        const object_type = object.constructor
        

        if (object_type == HTMLButtonElement) { return this.id_from_button(object) }

        if (object_type == HTMLTextAreaElement) { return this.id_from_textarea(object) }

        if (object_type == HTMLDivElement) { return this.id_from_div(object) }

        if (object_type == File) { return this.id_from_file(object) }

        
        throw new Error("File id is undefined")
    },




    get_class(object) {
        const object_class = object.getAttribute("class")
        
        if(!object_class) throw new Error("Fail to obtain object class.")

        return object_class
    },

    id_from_button(object) {
        const object_class = this.get_class(object)

        if (object_class.includes("delete")) return this.id_from_dropdown_menu_button(object)

        if (object_class.includes("save")) return this.id_from_dropdown_menu_button(object)

        if (object_class.includes("file")) return this.id_from_file_button(object)
        
        if (object_class.includes("tab")) return this.id_from_file_button(object)
        

        throw new Error("Fail to obtain id from 'HTMLButtonElement'.") 
    },

    id_from_dropdown_menu_button(object) {
        const items = $(object).parent()
        const menu = items.parent()
        const dropdown_menu = menu.parent()
        const panel = dropdown_menu.parent()

        const id = panel.attr("file-id") 
        
        if (!id) throw new Error("Fail to obtain id from delete button.") 

        return id
    },

    id_from_file_button(object) {
        const id = object.getAttribute("file-id")

        if(!id) throw new Error("Fail to obtain id from left button.")

        return id
    },

    // id_from_save_button(object) {

    // },



    id_from_div(object) {
        const dropdown_menu = $(object).parent()
        const panel = dropdown_menu.parent()
        
        const id = panel.attr("file-id")
        if (!id) throw new Error("Fail to obtain id from 'HTMLDivElement'.") 
        
        return id
    },



    id_from_file(object) {
        const id = object.id
        if (!id) throw new Error("Fail to obtain id from 'File object'.") 

        return id
    },



    id_from_textarea(object) {
        const input_field = $(object).parent()
        const form = input_field.parent()
        const panel = form.parent()

        const id = panel.attr("file-id")
        if (!id) throw new Error("Fail to obtain id from 'HTMLTextAreaElement'.") 

        return id
    },
}