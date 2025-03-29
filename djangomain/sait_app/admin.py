from django.contrib import admin, messages
from sait_app.models import Author, Publisher, Tag
# from django.utils.safestring import mark_safe


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'photo_author', 'slug', 'ful_name', ]
    fields = []
    list_display_links = ['first_name', 'last_name', ]
    list_editabl = ['slug', ]
    list_filter = ['publisher__publisher_name', 'tag__tag']
    list_select_related = []
    ordering = ['pk']
    search_fields = ['first_name', 'last_name', ]
    search_help_text = 'поиск по имени и фамилии'
    filter_horizontal = ['publisher']
    radio_fields = {"tag": admin.HORIZONTAL}
    prepopulated_fields = {'slug': ('first_name', 'last_name', )}

    @admin.display(description='полное имя')
    def ful_name(self, item: Author):
        return '{} {}'.format(item.first_name, item.last_name, )

    # @admin.display(description='фотокарта')
    # def admin_photo(self, item: Author):
    #     return mark_safe(f"<img src='{{ author_objects.photo_author.url }}' width=50>")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['publisher_name', 'slug', 'popularity', 'publisher_content' ]
    actions = ['low_popularity', 'medium_popularity', 'high_popularity', ]
    list_editabl = ['popularity', 'publisher_name', ]

    def action_popularity(self, request, queryset, arg):
        items = queryset.update(popularity=arg)
        message = '{} обекта изменено'.format(items)
        admin.ModelAdmin.message_user(self, request, message, level=messages.INFO)

    @admin.action(description='изменить на низкий уровеннь популярности')
    def low_popularity(self, request, queryset):
        self.action_popularity(request, queryset, 'low')

    @admin.action(description='изменить на средний уровеннь популярности')
    def medium_popularity(self, request, queryset):
        self.action_popularity(request, queryset, 'medium')

    @admin.action(description='изменить на высокий уровеннь популярности')
    def high_popularity(self, request, queryset):
        self.action_popularity(request, queryset, 'high')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'slug']


admin_staf = admin.sites.AdminSite
admin_staf.site_header = 'командный мостик капитана корабля'
# admin_staf.site_title = 'бортовая навигация'
admin_staf.index_title = 'бортовая навигация'
