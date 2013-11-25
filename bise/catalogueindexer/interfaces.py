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
