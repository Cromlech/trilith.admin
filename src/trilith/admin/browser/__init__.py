# -*- coding: utf-8 -*-

@view_component
@name('add')
@context()
class Add(Form):

    ignoreContent = True
    ignoreRequest = False

    responseFactory = Response
    make_response = form_response
    label = u"Données de la Feuille"
    dataValidators = [InvariantsValidation]

    template = tal_template('form.cpt')
    
    @property
    def fields(self):
        return Fields(*schema.get(self.context.mod.Batch.model))

    @property
    def action_url(self):
        return '%s/batch/add_sheet' % str(self.request.script_name)
        
    def update(self):
        complete.need()
        Form.update(self)

    @action(u"Créer la feuille")
    def create(self):
        data, errors = self.extractData()

        if errors:
            self.submissionError = errors
	    print errors
            return FAILURE

        model = self.context.mod.Batch.model()
        utils.set_fields_data(self.fields, model, data)
        self.context.add(model)

        url = str(self.request.script_name)
        action_url = '%s/batch/sheets/%s/add_entry' % (url, model.feuille)
        website_message(u"Feuille créée avec succès.")
        raise exceptions.HTTPFound(location=action_url)
        
    @action(u"Annuler")
    def cancel(self):
        action_url = str(self.request.script_name) + '/batch'
        website_message(u"Saisie interrompue.")
        raise exceptions.HTTPFound(location=action_url)
