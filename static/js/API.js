class API   {
    constructor() {
        Object.assign(this, IdMixin, PanelsMixin)
        Object.assign(this, 
            FilesMixin, SaveFileMixin, FileMenuMixin,
            OpenFileMixin, CloseFileMixin,
            CreateFileMixin, DeleteFileMixin,            
        )

        this.panels = {
            left: new LeftPanel(),
            top: new TopPanel(),
        }
        this.files = {
            start_creating: this.start_creating.bind(this),
            start_deleting: this.start_deleting.bind(this),
            
            open: this.open_file.bind(this),
            close: this.close_file.bind(this),
            save: this.save_file.bind(this),
            
            
            all: this.collect_files(),
            opened: Array(),
            active: null,
            next: null,
        }
        this.forms = {
            deletion: new FileDeletionForm(),
            creation: new FileCreationForm(this.files)
        }
    }
}

