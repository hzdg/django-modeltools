import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=[], exclude=[], header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """

    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta

        if len(fields) > 0:
            field_names = [field.name for field in opts.fields \
                    if field.name not in exclude and field.name in fields]
        else:
            field_names = [field.name for field in opts.fields \
                    if field.name not in exclude]

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % \
                                            unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([smart_str(
                                getattr(obj, field)) for field in field_names])
        return response

    export_as_csv.short_description = description
    return export_as_csv
