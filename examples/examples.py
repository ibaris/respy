class UfuncHelpers(dict):
    """Registry of unit conversion functions to help ufunc evaluation.

    Based on dict for quick access, but with a missing method to load
    helpers for additional modules such as scipy.special and erfa.

    Such modules should be registered using ``register_module``.
    """
    UNSUPPORTED = set()

    def register_module(self, module, names, importer):
        """Register (but do not import) a set of ufunc helpers.

        Parameters
        ----------
        module : str
            Name of the module with the ufuncs (e.g., 'scipy.special').
        names : iterable of str
            Names of the module ufuncs for which helpers are available.
        importer : callable
            Function that imports the ufuncs and returns a dict of helpers
            keyed by those ufuncs.  If the value is `None`, the ufunc is
            explicitly *not* supported.
        """
        self.modules[module] = {'names': names,
                                'importer': importer}

    @property
    def modules(self):
        """Modules for which helpers are available (but not yet loaded)."""
        if not hasattr(self, '_modules'):
            self._modules = {}
        return self._modules

    def import_module(self, module):
        """Import the helpers from the given module using its helper function.

        Parameters
        ----------
        module : str
            Name of the module. Has to have been registered beforehand.
        """
        module_info = self.modules.pop(module)
        self.update(module_info['importer']())

    def __missing__(self, ufunc):
        """Called if a ufunc is not found.

        Check if the ufunc is in any of the available modules, and, if so,
        import the helpers for that module.
        """
        if ufunc in self.UNSUPPORTED:
            raise TypeError("Cannot use ufunc '{0}' with quantities"
                            .format(ufunc.__name__))

        for module, module_info in list(self.modules.items()):
            if ufunc.__name__ in module_info['names']:
                # A ufunc with the same name is supported by this module.
                # Of course, this doesn't necessarily mean it is the
                # right module. So, we try let the importer do its work.
                # If it fails (e.g., for `scipy.special`), then that's
                # fine, just raise the TypeError.  If it succeeds, but
                # the ufunc is not found, that is also fine: we will
                # enter __missing__ again and either find another
                # module or get the TypeError there.
                try:
                    self.import_module(module)
                except ImportError:
                    pass
                else:
                    return self[ufunc]

        raise TypeError("unknown ufunc {0}.  If you believe this ufunc "
                        "should be supported, please raise an issue on "
                        "https://github.com/astropy/astropy"
                        .format(ufunc.__name__))

    def __setitem__(self, key, value):
        # Implementation note: in principle, we could just let `None`
        # mean that something is not implemented, but this means an
        # extra if clause for the output, slowing down the common
        # path where a ufunc is supported.
        if value is None:
            self.UNSUPPORTED |= {key}
            self.pop(key, None)
        else:
            super(UfuncHelpers, self).__setitem__(key, value)
            self.UNSUPPORTED -= {key}