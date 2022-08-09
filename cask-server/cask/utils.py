from django.db.models import ForeignKey
from graphene.utils.str_converters import to_camel_case


# https://github.com/graphql-python/graphene/issues/348#issuecomment-267717809
def get_selected_names(info):
    """
    Parses a query info into a list of composite field names.

    For example the following query:

        {
          carts {
            id
            name
            ...cartInfo
            }
        }
        fragment cartInfo on CartType { whatever }

    Will result in an array:

        [
            'carts',
            'carts.id',
            'carts.name',
            'carts.whatever'
        ]
    """
    from graphql.language.ast import FragmentSpread

    fragments = info.fragments

    def iterate_field_names(prefix, field):
        name = field.name.value

        if isinstance(field, FragmentSpread):
            results = []
            new_prefix = prefix
            sub_selection = fragments[field.name.value].selection_set.selections
        else:
            results = [prefix + name]
            new_prefix = prefix + name + "."
            sub_selection = (
                field.selection_set.selections if field.selection_set else []
            )

        for sub_field in sub_selection:
            results += iterate_field_names(new_prefix, sub_field)

        return results

    results = iterate_field_names("", info.field_asts[0])
    return results


def optimize_queryset(qs, info, root):
    """
    Pulls in available database relations to avoid N+1 queries.

    For example the following query:

        {
          carts {
            id
            name
            ...cartInfo
            }
        }
        fragment cartInfo on CartType {
            store {
                id
                name
            }
        }

    It will automatically pull in the 'store' relation (assuming its a ForeignKey
    or ManyToMany) using the ORM.

    >>> qs = Cart.objects.all()
    >>> optimize_queryset(qs, info, 'carts')
    """
    # right now we're only handling one level deep
    root_len = len(to_camel_case(root)) + 1
    selected_fields = set(
        [x[root_len:] if x.startswith(root) else x for x in get_selected_names(info)]
    )
    select = []
    for field in qs.model._meta.fields:
        field_name = to_camel_case(field.name)
        if field_name in selected_fields:
            if isinstance(field, ForeignKey):
                select.append(field.name)
    if select:
        qs = qs.select_related(*select)

    prefetch = []
    for field in qs.model._meta.many_to_many:
        field_name = to_camel_case(field.name)
        if field_name in selected_fields:
            prefetch.append(field.name)
    if prefetch:
        qs = qs.prefetch_related(*prefetch)
    return qs
