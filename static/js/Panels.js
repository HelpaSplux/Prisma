class Panel {
	constructor(classes) {
		this.classes = classes
		this.buttons = {
			all: this.collect_buttons(),
			create: this.add_button.bind(this),
			get size() {return this.all.size},
		}
		this.objects = this.configure_objects()
	}


	configure_objects() {
		const objects = {
			self: $(`.${this.classes.self}`),
			list: $(`.${this.classes.list}`),
			button: $(`.${this.classes.button}`),
		}

		return objects
	}

	collect_buttons() {
		const buttons = new Map()
		const button_elements = $("." + this.classes.button)
		
		for (let element of button_elements) {
			let button = new Button(element)
			buttons.set(button.id, button)
		}

		return buttons
	}

	add_button(title, id) {
		if (!id) { id = this.buttons.size }	

		let button = `<button class="${this.classes.button}" file-id="${id}" type="button">${title}</button>`
		this.objects.list.append(button)

		button = this.objects.list.find(`[file-id='${id}']`)
		button = new Button(button)
		this.buttons.all.set(button.id, button)

		this.scroll_to(button)
		button.highlight()

		return button
	}

	remove(id) {
		const buttons = this.buttons.all
		const button = buttons.get(id)
		
		button.remove()
		buttons.delete(id)
		return
	}


	scroll_to(button) {
		button = button.objects.self[0]
		button.scrollIntoView({
			behavior: "smooth",
			block: "center"
		})
	} 

}



class TopPanel extends Panel {
	constructor() {
		let classes = {
			self: "top_panel",
			list: "tab_bar",
			button: "tab_button",
		}
		super(classes)
	}

	move_button(button) {
		const id = button.id
		
		// Class
		this.buttons.all.delete(id)
		this.buttons.all.set(id, button)


		// Template
		button.objects.self.remove()
		this.objects.list.append(button.objects.self)
	}
}



class LeftPanel extends Panel {
	constructor() {
		const classes = {
			self: "bottom_left_panel",
			list: "file_list",
			button: "file_button",
			toggle: "hidden",
		}
		super(classes)
		this.url = this.objects.list.attr("href")
		this.displayed = this.is_visible()
	}



	toggle() {
	    const panel_visible = this.displayed
	    
		if (panel_visible) { return this.hide() }

	    if (!panel_visible) { return this.show() }

		throw new Error("Fail to toggle left panel.")
	}

	show() {
		const toggle = this.classes.toggle
		const panel = this.objects.self

		panel.removeClass(toggle)
		this.displayed = this.is_visible()
	}
	hide() {
		const toggle = this.classes.toggle
		const panel = this.objects.self

		panel.addClass(toggle)
		this.displayed = this.is_visible()
	}


	is_visible() {
		const toggle = this.classes.toggle
		const current_panel_class = this.objects.self.attr("class")
		const status = !current_panel_class.includes(toggle)

		return status
	}
}

class RightPanel {
	classes = {
		self: "bottom_right_panel",
		form: "file-update-form",
		
		label: "label_field",
		content: "content_field",
		
		toggle: "active",
	}

    constructor(panel, id) {
		this.objects = this.configure(panel, id)
        this.resizeTextareas() 
    }

	get label() {
		return this.objects.form.textarea.label
	}
	
	get content() {
		return this.objects.form.textarea.content
	}

	get url() {
		return this.objects.form.url
	}
	
	get csrf_token() {
		return this.objects.form.csrf_token
	}
	
	get menu() {
		return this.objects.menu
	}


	get_form(self) {
		const form = self.find("." + this.classes.form)
		const url = form.attr("action")
        const csrf_token = form.find("input[name=csrfmiddlewaretoken]").val()

		// Fields
		const label = form.find(`[class='${this.classes.label}']`)
		const content = form.find(`[class='${this.classes.content}']`)

		const form_object = {
			self: form,
			url: url,
			csrf_token: csrf_token,
			textarea: {
				label: label,
				content: content,	
			}
		}
		return form_object
	}

	configure(panel, id) {
		const content = $(".content")
		content.append(panel)
		

		const self = content.find(`[class='${this.classes.self}'][file-id='${id}']`)
		const menu = new DropdownMenu(self)
		const form = this.get_form(self)
		

		const objects = {
			content: content,
			self: self,
			menu: menu,
			form: form,
		}
		return objects	
	}


    resizeTextareas() {
		const textarea = this.objects.form.textarea
		const label = textarea.label
		const content = textarea.content

        this.resizeTextarea(label)
        this.resizeTextarea(content)

		return
    }
    resizeTextarea(textarea) {
        textarea.css("height", "auto")
        textarea.css("height", `${textarea.prop("scrollHeight")}px`)
		
		return
    }


    show() {
		const self = this.objects.self
		const toggle = this.classes.toggle

        self.addClass(toggle)

		return
    }
    hide() {
		const self = this.objects.self
		const toggle = this.classes.toggle

        self.removeClass(toggle)

		return
    }

	remove() {
		this.objects.self.remove()
		return
	}
}



class Button {
	classes = {
		active: "active",
		created: "created",
		toggle: "hidden",
	}

    constructor(button) {
		button = $(button)
		
		this.classes.self = button.attr("class")
		this._name = button.text()
		this.id = button.attr("file-id")

        this.objects = this.configure_objects()
    }

	get name() {
		return this._name
	}
	set name(new_name) {
		this.objects.self.text(new_name)
		this._name = new_name
	}

	configure_objects() {
		const objects = {
			self: $(`[class='${this.classes.self}'][file-id='${this.id}']`),
		}

		return objects
	}

    highlight() {	
		const button = this.objects.self
		button.addClass(this.classes.created);
		setTimeout(() => {button.removeClass(this.classes.created)}, 1500);
	}

    show() { this.objects.self.removeClass(this.classes.toggle) }
    hide() { this.objects.self.addClass(this.classes.toggle) }

    activate() { this.objects.self.addClass(this.classes.active) }
    deactivate() { this.objects.self.removeClass(this.classes.active) }

	remove() {
		const self = this.objects.self

		self.remove()
		
		return
	}
}




class DropdownMenu {
	classes = {
		self: "dropdown-menu",
		button: "dropdown",
		items: "items",
		toggle: "active",
	}


    constructor(object) {
		const button = this.classes.button
		const self = this.classes.self
		const items = this.classes.items

		this.objects = {
			button: object.find(`.${button}`),
        	items: object.find(`.${self} .${items}`),
		}
    }


    togle() {
		const button = this.objects.button
		const toggle = this.classes.toggle

        const current_class = button.attr("class")
        const button_active = current_class.includes(toggle)

        if (button_active) {
            this.deactivate()
			return
        }
        if (!button_active) {
            this.activate()
			return
        }

		throw new Error("Fail to toggle menu.")
    }


    activate() {
		const toggle = this.classes.toggle
		const button = this.objects.button
		const items = this.objects.items

        button.addClass(toggle)
        items.addClass(toggle)
        this.add_listener()

		return
    }

    deactivate() {
		const toggle = this.classes.toggle
		const button = this.objects.button
		const items = this.objects.items

        button.removeClass(toggle)
        items.removeClass(toggle)
        this.remove_listener()

		return
    }




    on_click(event) {
        const target = $(event.target)
		const self = this.classes.self
		const click_inside_menu = target.closest(`.${self}`).length

        if(!click_inside_menu) {this.deactivate()}

		return
    }

    add_listener() { $(document).on("click.dropdown", "body", this.on_click.bind(this)) }
    remove_listener() { $(document).off("click.dropdown") }

}