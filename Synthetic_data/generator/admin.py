from django.contrib import admin
from .models import Metadata, Synthesizer
import openpyxl
from django.utils.html import format_html
from django.contrib import admin
from .models import ExcelFile

# Custom admin class for Metadata model
class MetadataAdmin(admin.ModelAdmin):
    # List the fields to display in the list view (admin panel)
    list_display = ('name', 'description', 'created_at')  # Fields to display
    search_fields = ('name', 'description')  # Enable search by name and description
    list_filter = ('created_at',)  # Filter by the date the metadata was created
    ordering = ('-created_at',)  # Order by the creation date (newest first)

# Register the models with the admin panel and the custom admin class
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Synthesizer)

@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at', 'show_excel_button')  # Add the button
    search_fields = ('name',)
    list_filter = ('uploaded_at',)

    # Add a button to show the Excel data
    def show_excel_button(self, obj):
        return format_html('<a class="button" href="{}">Show Excel File</a>', obj.file.url)

    show_excel_button.short_description = 'Show Excel File'

    # Show the Excel file contents when clicked
    def changelist_view(self, request, extra_context=None):
        if "show_excel" in request.GET:
            file_id = request.GET["show_excel"]
            excel_file = ExcelFile.objects.get(id=file_id)
            data = self.parse_excel(excel_file)
            return self.render_change_form(request, extra_context={'data': data})
        return super().changelist_view(request, extra_context=extra_context)

    def parse_excel(self, excel_file):
        wb = openpyxl.load_workbook(excel_file.file.path)
        sheet = wb.active
        rows = sheet.iter_rows(values_only=True)
        data = [row for row in rows]  # Parse all rows into a list of tuples
        return data