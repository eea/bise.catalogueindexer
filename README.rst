Introduction
============

Event handlers to index BISE site content in BISE Catalogue.


How this works
-----------------

This package provides 3 event listeners for basic plone content-types (based on
plone.app.contenttypes). These event listeners adapt the context object
to Catalogue resource types (Article, Document or Link), get the relevant information
and then index in the catalogue.

This package provides basic adapters for plone.app.contenttypes provided content-types,
if you need more specific adapters for your content-types, just create an adapter
for it.
