from bise.catalogueindexer.interfaces import ICatalogueIndexerSettings
from logging import getLogger
from plone import api
from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.registry.interfaces import IRegistry
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component import getUtility
from StringIO import StringIO

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
            files = {}
            if 'document[file]' in items:
                files['document[file]'] = items.get('document[file]')
                del items['document[file]']

            resp = requests.post(
                url,
                data=items,
                files=files,
            )
            if not resp.ok:
                log = getLogger('index_creation')
                log.info('Error indexing creation of {0}'.format(
                    '/'.join(self.context.getPhysicalPath())
                    )
                )

    def index_update(self):
        url = self._get_catalog_url()
        items = self.get_values_to_index()
        if items and url:
            items['source_url'] = self.context.absolute_url()
            files = {}
            if 'document[file]' in items:
                files['document[file]'] = items.get('document[file]')
                del items['document[file]']

            resp = requests.put(
                url,
                data=items,
                files=files,
            )
            if not resp.ok:
                log = getLogger('index_update')
                log.info('Error updating {0}'.format(
                    '/'.join(self.context.getPhysicalPath())
                    )
                )

    def index_delete(self):
        url = self._get_catalog_url()
        if url:
            items = {}
            ditems = self.get_values_to_index()
            items['resource_type'] = ditems.get('resource_type', '')
            items['source_url'] = self.context.absolute_url()
            resp = requests.delete(
                url,
                data=items,
            )
            if not resp.ok:
                log = getLogger('index_delete')
                log.info('Error deleting {0}'.format(
                    '/'.join(self.context.getPhysicalPath())
                    )
                )


class PACDocumentCataloguer(BaseObjectCataloguer):

    def get_values_to_index(self):
        context = self.context
        try:
            metadata = IDublinCore(context)
            items = {}
            # XXX
            user = api.user.get(context.Creator())
            fullname = user.getProperty('fullname') or user.getId()
            items['article[site_id]'] = self._get_catalog_site_id()
            # should be context.creator
            items['article[author]'] = fullname
            # XXX hardcoded. should be context.language
            items['article[language_ids]'] = '6'
            items['article[title]'] = metadata.title
            items['article[english_title]'] = metadata.title
            created = context.created().strftime('%d/%m/%Y')
            items['article[published_on]'] = created
            try:
                if api.content.get_state(obj=context) == 'published':
                    items['article[approved]'] = True
                    if metadata.effective:
                        effective = metadata.effective.strftime('%d/%m/%Y')
                    else:
                        effective = DateTime.DateTime().strftime('%d/%m/%Y')
                    items['article[approved_at]'] = effective
                else:
                    items['article[approved]'] = False
                    items['article[approved_at]'] = u''
            except WorkflowException:
                items['article[approved]'] = True
                items['article[approved_at]'] = created

            items['article[source_url]'] = context.absolute_url()
            content = metadata.description + u' ' + context.text.output
            items['article[content]'] = content
            items['resource_type'] = 'article'
            return items
        except:
            return {}


class PACFileCataloguer(PACDocumentCataloguer):

    def get_values_to_index(self):
        context = self.context
        items = {}
        user = api.user.get(context.Creator())
        fullname = user.getProperty('fullname') or user.getId()
        items['document[site_id]'] = self._get_catalog_site_id()
        # should be context.creator
        items['document[author]'] = fullname
        # XXX hardcoded. should be context.language
        items['document[language_ids]'] = '6'
        items['document[title]'] = context.title
        items['document[english_title]'] = context.title
        created = context.created().strftime('%d/%m/%Y')
        items['document[published_on]'] = created
        try:
            if api.content.get_state(obj=context) == 'published':
                items['document[approved]'] = True
                if context.effective:
                    effective = context.contexteffective.strftime('%d/%m/%Y')
                else:
                    effective = DateTime.DateTime().strftime('%d/%m/%Y')
                items['document[approved_at]'] = effective
            else:
                items['document[approved]'] = False
                items['document[approved_at]'] = u''
        except WorkflowException:
            items['document[approved]'] = True
            items['document[approved_at]'] = created

        items['document[source_url]'] = context.absolute_url()

        items['document[description]'] = context.description
        filedata = (context.file.filename, StringIO(context.file.data))
        items['document[file]'] = filedata
        items['resource_type'] = 'document'

        return items


class PACLinkCataloguer(PACDocumentCataloguer):

    def get_values_to_index(self):
        context = self.context
        items = {}
        user = api.user.get(context.Creator())
        fullname = user.getProperty('fullname') or user.getId()
        items['link[site_id]'] = self._get_catalog_site_id()
        # should be context.creator
        items['link[author]'] = fullname
        # XXX hardcoded. should be context.language
        items['link[language_ids]'] = '6'
        items['link[title]'] = context.title
        items['link[english_title]'] = context.title
        created = context.created().strftime('%d/%m/%Y')
        items['link[published_on]'] = created
        try:
            if api.content.get_state(obj=context) == 'published':
                items['link[approved]'] = True
                if context.effective:
                    effective = context.effective.strftime('%d/%m/%Y')
                else:
                    effective = DateTime.DateTime().strftime('%d/%m/%Y')
                items['link[approved_at]'] = effective
            else:
                items['link[approved]'] = False
                items['link[approved_at]'] = u''
        except WorkflowException:
            items['link[approved]'] = True
            items['link[approved_at]'] = created

        items['link[source_url]'] = context.absolute_url()

        items['link[description]'] = context.description
        items['link[url]'] = context.remoteUrl
        items['resource_type'] = 'link'

        return items
