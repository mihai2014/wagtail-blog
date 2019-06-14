# Generated by Django 2.2.1 on 2019-06-14 13:56

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190614_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('two_columns', wagtail.core.blocks.StructBlock([('left_column', wagtail.core.blocks.StreamBlock([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('htmljs', wagtail.core.blocks.TextBlock()), ('code_bash', wagtail.core.blocks.TextBlock()), ('code_py', wagtail.core.blocks.TextBlock()), ('code_htmljs', wagtail.core.blocks.TextBlock())], icon='arrow-right', label='Left column content')), ('right_column', wagtail.core.blocks.StreamBlock([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('htmljs', wagtail.core.blocks.TextBlock()), ('code_bash', wagtail.core.blocks.TextBlock()), ('code_py', wagtail.core.blocks.TextBlock()), ('code_htmljs', wagtail.core.blocks.TextBlock())], icon='arrow-right', label='Right column content'))])), ('three_columns', wagtail.core.blocks.StructBlock([('column1', wagtail.core.blocks.StreamBlock([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('htmljs', wagtail.core.blocks.TextBlock()), ('code_bash', wagtail.core.blocks.TextBlock()), ('code_py', wagtail.core.blocks.TextBlock()), ('code_htmljs', wagtail.core.blocks.TextBlock())], icon='arrow-right', label='Column 1')), ('column2', wagtail.core.blocks.StreamBlock([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('htmljs', wagtail.core.blocks.TextBlock()), ('code_bash', wagtail.core.blocks.TextBlock()), ('code_py', wagtail.core.blocks.TextBlock()), ('code_htmljs', wagtail.core.blocks.TextBlock())], icon='arrow-right', label='Column 2')), ('column3', wagtail.core.blocks.StreamBlock([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('htmljs', wagtail.core.blocks.TextBlock()), ('code_bash', wagtail.core.blocks.TextBlock()), ('code_py', wagtail.core.blocks.TextBlock()), ('code_htmljs', wagtail.core.blocks.TextBlock())], icon='arrow-right', label='Column 3'))])), ('image_center', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(icon='image', label='Image Center')), ('caption', wagtail.core.blocks.TextBlock(icon='placeholder', label='caption'))])), ('image_left', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(icon='image', label='Image Left')), ('caption', wagtail.core.blocks.TextBlock(icon='placeholder', label='caption'))]))], blank=True, null=True),
        ),
    ]
