from wagtail.core.models import PageRevision

revisions = PageRevision.objects.all()

for rev in revisions:
    print(rev.id,rev.page)
    rev.delete()

