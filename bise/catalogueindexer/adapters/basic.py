from bise.catalogueindexer.interfaces import ICatalogueBase
from bise.catalogueindexer.interfaces import ICatalogueIndexerSettings
from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.registry.interfaces import IRegistry
from zope.component import adapts
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import provides

import requests


class BaseObjectCataloguer(object):
    """
    Base adapter. All other adapters should subclass
    this one, implement `get_values_to_index` method and
    be registered for the correct interface.

    Thus, the webservice interaction code is written just once.

    """
    adapts(Interface)
    provides(ICatalogueBase)

    def __init__(self, context):
        self.context = context

    def get_values_to_index(self):
        return {}

    def _get_catalog_url(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICatalogueIndexerSettings)
        return settings.catalogue_endpoint

    def _get_catalog_site_id(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICatalogueIndexerSettings)
        return settings.catalogue_siteid

    def index_creation(self):
        url = self._get_catalog_url()
        site_id = self._get_catalog_site_id()
        items = self.get_values_to_index()
        items.update({'site': site_id})
        r = requests.post(
            url,
            payload=items,
        )
        if r.status_code != requests.codes.ok:
            from logging import getLogger
            log = getLogger('index_creation')
            log.info('Error indexing creation of {0}'.format(
                '/'.join(self.context.getPhysicalPath())
                )
            )

    def index_update():
        items = self.get_values_to_index()
        raise NotImplementedError

    def index_delete():
        items = self.get_values_to_index()
        raise NotImplementedError
