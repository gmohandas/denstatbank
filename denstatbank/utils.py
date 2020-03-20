import pandas as pd


def data_dict_to_df(ddict, codes):
    """Augments a simple pandas dataframe to a multi-indexed dataframe from a
    list of key codes.
    """
    df = pd.DataFrame({ddict['label']: ddict['value']})
    dims = {k.lower(): v for k, v in ddict['dimension'].items()}
    keys = [k for k in dims.keys() if k in codes]
    vals = [list(dims[k]['category']['label'].values()) for k in keys]
    if len(vals) == len(keys) > 0:
        index = pd.MultiIndex.from_product(vals, names=keys)
        df.set_index(index, inplace=True)
    return df


def add_list_to_dict(d, **kwargs):
    """Adds keyword arguments whose values are lists to a given dictionary."""
    for k, v in kwargs.items():
        if v is not None:
            if isinstance(v, list):
                d.update({k: v})
            else:
                raise Exception(f'{k} must be a list.')


def subtabtree(d):
    """Generator to print tree structure of subjects and tables in db."""
    for k, v in d.items():
        if k == 'id':
            ival = d[k]
        if k == 'description' or k == 'text':
            dval = d[k]
            v = (ival, dval)
            yield f'\t |--{v}'
        if isinstance(v, list) and len(v) > 0:
            for i in v:
                if isinstance(i, dict):
                    for g in subtabtree(i):
                        yield f'\t |  {g}'
