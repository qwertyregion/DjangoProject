

class DataMixin:
    title_page = None

    def plus_mixin_data(self, context, **kwargs):
        if self.title_page is not None:
            context['title'] = self.title_page
        context.update(**kwargs)
        return context



