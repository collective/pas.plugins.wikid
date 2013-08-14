

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    import install
    install.register_wikid_plugin()
    install.register_wikid_plugin_class(context)
