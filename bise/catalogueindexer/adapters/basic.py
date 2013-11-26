from bise.catalogueindexer.interfaces import ICatalogueIndexerSettings
from logging import getLogger
from plone import api
from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import DateTime
import requests



class BaseObjectCataloguer(object):
    """
    Base adapter. All other adapters should subclass
    this one, implement `get_values_to_index` method and
    be registered for the correct interface.

    Thus, the webservice interaction code is written just once.

    """

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
        items = self.get_values_to_index()
        if items and url:
            resp = requests.post(
                url,
                data=items,
            )
            if not resp.ok:
                log = getLogger('index_creation')
                log.info('Error indexing creation of {0}'.format(
                    '/'.join(self.context.getPhysicalPath())
                    )
                )

    def index_update(self):
        raise NotImplementedError

    def index_delete(self):
        raise NotImplementedError


class PACCataloger(BaseObjectCataloguer):

    def get_values_to_index(self):
        context = self.context
        try:
            metadata = IDublinCore(context)
            items = {}
            # XXX
            user = api.user.get(context.Creator())
            items['article[site_id]'] = self._get_catalog_site_id()
            items['article[author]'] = user.getProperty('fullname') or user.getId() # should be context.creator
            items['article[language_ids]'] = '6' # hardcoded. should be context.language
            items['article[title]'] = metadata.title
            items['article[english_title]'] = metadata.title
            items['article[published_on]'] = context.created().strftime('%d/%m/%Y')
            if api.content.get_state(obj=context) == 'published':
                items['article[approved]'] = True
                if metadata.effective:
                    items['article[approved_at]'] = metadata.effective.strftime('%d/%m/%Y')
                else:
                    items['article[approved_at]'] = DateTime.DateTime().strftime('%d/%m/%Y')
            items['article[source_url]'] = context.absolute_url()
            items['article[content]'] = metadata.description + u' ' + context.text.output
            items['resource_type'] = 'article'
            return items
        except:
            return {}
