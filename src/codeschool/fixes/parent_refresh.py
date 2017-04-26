from modelcluster.forms import ClusterForm

PARENT_PREFETCH_CLASSES = set()


#
# We patch ClusterForm to make it support classes with inline models that
# requires a parent reference for validation
#
class ClusterFormPatch:

    def is_valid(self):
        form_is_valid = super(ClusterForm, self).is_valid()
        prefetch = self.requires_parent_prefetch()

        # Save instance on formsets before checking its validity
        for formset in self.formsets.values():
            if prefetch:
                self.prefetch(self.instance, formset)
            form_is_valid &= formset.is_valid()

        return form_is_valid

    def requires_parent_prefetch(self):
        """
        Return True if form requires parent injection
        """

        return self.is_bound and self.Meta.model in PARENT_PREFETCH_CLASSES

    def prefetch(self, parent, formset):
        """
        Prefetch the parent relation to the children bound to a formset.
        """

        relation = formset.fk.name
        for form in formset.forms:
            setattr(form.instance, relation, parent)


for _k, _v in vars(ClusterFormPatch).items():
    if not _k.startswith('_'):
        setattr(ClusterForm, _k, _v)


def register_parent_prefetch(cls):
    """
    Register class so that parent gets calculated and bound to each formset
    before calling .is_valid() for each formset.
    """

    PARENT_PREFETCH_CLASSES.add(cls)
    return cls
