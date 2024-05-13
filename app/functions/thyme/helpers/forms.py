def prepopulate_form(form, item):
    for field in form:
        if (field.widget.input_type != 'hidden' and field.type != 'SubmitField'):
            field = getattr(form, field.name)
            value = getattr(item, field.name)
            setattr(getattr(form, field.name), 'data', value)