from zope import schema
from zope.interface import Interface

from bise.catalogueindexer import CatalogueIndexerMessageFactory as _


class ICatalogueIndexerSettings(Interface):
    """
    Configuration values for Catalogue available through plone.app.registry
    """

    catalogue_endpoint = schema.TextLine(
        title=_(u'Catalogue API endpoint'),
        description=_(u'Enter the full URL of the catalogue API, '
                      u'where the queries will be directed to'
            )
    )

    catalogue_siteid = schema.TextLine(
        title=_(u'Site identifier for the Catalogue'),
        description=_(u"Enter this site's identifier in the catalog. If "
                      u"unkown, ask catalogue admins for this value."
            )
    )


class ICatalogueBase(Interface):

    title = schema.TextLine(
        title=_(u"Resource title"),
        required=True,
    )

    site = schema.TextLine(
        title=_(u"Site id"),
        required=True,
    )

    english_title = schema.TextLine(
        title=_(u"Resource's english title"),
        required=True,
    )

    author = schema.TextLine(
        title=_(u"Resource's author"),
        required=True,
    )

    language_ids = schema.TextLine(
        title=_(u"Resource's language ids"),
        required=True,
    )

    published_on = schema.TextLine(
        title=_(u"Resource's publication date in dd/mm/yyyy format"),
        required=True,
    )

    source_uri = schema.TextLine(
        title=_(u"Resource's URI"),
        required=True,
    )


class ICatalogueArticle(ICatalogueBase):

    content = schema.TextLine(
        title=_(u"Resource's content"),
        required=True,
    )


class ICatalogueDocument(ICatalogueBase):

    file = schema.TextLine(
        title=_(u"Resource file"),
        required=True,
    )

    description = schema.TextLine(
        title=_(u"Resource's description"),
        required=True,
    )


class ICatalogueLink(ICatalogueBase):

    url = schema.TextLine(
        title=_(u"Resource url"),
        required=True,
    )

    description = schema.TextLine(
        title=_(u"Resource's description in text/html"),
        required=True,
    )
