from bise.catalogueindexer.interfaces import ICatalogueBase
from zope.component import queryAdapter


def create_item(obj, event):
    adapter = queryAdapter(obj, ICatalogueBase)
    if adapter is not None:
        adapter.index_creation()


def update_item(obj, event):
    adapter = queryAdapter(obj, ICatalogueBase)
    if adapter is not None:
        adapter.index_update()


def delete_item(obj, event):
    adapter = queryAdapter(obj, ICatalogueBase)
    if adapter is not None:
        adapter.index_delete()
