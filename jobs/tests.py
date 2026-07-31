from pathlib import Path

from django.apps import apps
from django.template.loader import get_template
from django.test import SimpleTestCase


class TemplateCompilationTests(SimpleTestCase):
    def test_all_application_templates_compile(self):
        """Empêche la mise en ligne d'une balise Django mal fermée."""
        template_names = []
        for app_config in apps.get_app_configs():
            template_directory = Path(app_config.path) / "templates"
            if template_directory.exists():
                template_names.extend(
                    template_file.relative_to(template_directory).as_posix()
                    for template_file in template_directory.rglob("*.html")
                )

        for template_name in sorted(template_names):
            with self.subTest(template=template_name):
                get_template(template_name)
