class Notification {
    message_class = "message"
    delay = 3000


    constructor(data) {
        if (!data.status) {
            this.message_type = "success"
            this.message = data.message
        }
        else {
            this.message_type = "error"
            this.message = data.responseJSON.message
        }

        this.create_element()
        this.find_this_element()

        this.show()
        this.hide()
    }

    create_element() {
        let element = `<div class="${this.message_class}">${this.message}</div>`;
        let body = $("body");
        body.append(element);
    }
    
    find_this_element() {
        let messages = $("." + this.message_class);
        this.element = $(messages[messages.length -1]);
    }
    
    show() {
        setTimeout(() => { this.element.addClass(this.message_type) }, 0);
    }

    hide() {
        setTimeout(() => { this.element.removeClass(this.message_type) }, this.delay);
        setTimeout(() => { this.element.remove() }, this.delay * 2);
    }

}