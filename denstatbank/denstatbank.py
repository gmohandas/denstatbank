import requests
import pandas as pd
from urllib.parse import quote
from .utils import data_dict_to_df, add_list_to_dict, subtabtree


class StatBankClient:
    def __init__(self, lang='da'):
        self._lang = lang
        self.session = requests.session()
        self._base_url = 'https://api.statbank.dk/v1/'

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        if value not in ['en', 'da']:
            raise ValueError('Language can only accept either "en" or "da" as values.')
        self._lang = value

    def base_request(self, cat, params):
        params.update({'lang': self.lang})
        try:
            resp = self.session.post(self._base_url+quote(cat), json=params)
            if resp.status_code == 200:
                return resp.json()
            else:
                response_message = resp.json()['message']
                print(response_message)
        except Exception as err:
            print(err)

    def subjects(self, subjects=None, include_tables=False, recursive=False, as_tree=True):
        """Retrieves the basic subject(s) information for which tables exist in
        the StatBank database.

        Parameters
        ----------
        subjects : list, default is None
            list of subject id strings
        include_tables : bool, default is False
            if True, returns list of table information attached to subject id.
        recursive : bool, default is False
            if True, subtopics/tables will be retrieved all the way down the
            hierarchy.
        as_tree : bool, default is True
            prints a tree structure of the subjects heirarchy.
            Also prints tables if include_tables is True.
            Each item is a tuple with (subject/table id, description/text)
            Note: subject id's are numeric characters whereas table id's
            are alphanumeric.
            If False, returns a list of dictionaries.

        Returns
        -------
        list of dicts, or prints a tree structure.
        """
        cat = 'subjects'
        params = dict(includeTables=include_tables, recursive=recursive)
        add_list_to_dict(params, subjects=subjects)
        resp = self.base_request(cat, params)
        if not as_tree:
            return resp
        else:
            if len(resp) > 0:
                for d in resp:
                    for g in subtabtree(d):
                        print(g)

    def tables(self, subjects=None, past_days=None, include_inactive=False, as_df=True):
        """Retrieves the complete list of tables present currently in the
        Statbank database together with relevant metadata.

        Parameters
        ----------
        subjects : list, default is None
            If provided, returns tables attached to subject id.
        past_days : int, default is None
            number of days from present time for which updated tables are
            available.
        include_inactive : bool, default is False
            if True, includes tables that are no longer active.
        as_df : bool, default is True
            If true, returns a pandas dataframe, otherwise returns a list of
            dictionaries.

        Returns
        -------
        pd.DataFrame or list of dicts
        """
        cat = 'tables'
        params = dict(pastdays=past_days, includeinactive=include_inactive)
        add_list_to_dict(params, subjects=subjects)
        rjson = self.base_request(cat, params)
        if as_df:
            return pd.DataFrame(rjson)
        else:
            return rjson

    def tableinfo(self, table_id, variables_df=False):
        """Retrieves table specific information from the StatBank database.

        Parameters
        ----------
        table_id : str
        variables_df : bool, default is False
            If true, returns the variable names and possible values as a
            pandas dataframe, otherwise returns a dictionary including
            additional metadata.

        Returns
        -------
        dict or pd.DataFrame
        """
        cat = 'tableinfo'
        params = dict(table=table_id)
        rjson = self.base_request(cat, params)
        if variables_df:
            var_df = pd.DataFrame()
            varlist = rjson['variables']
            for d in varlist:
                df = pd.DataFrame(d['values'])
                if params['lang'] == 'en':
                    df['variable'] = d['text']
                else:
                    df['variable'] = d['id']
                var_df = var_df.append(df)
            return var_df
        else:
            return rjson

    def data(self, table_id, as_df=True, variables=None, **kwargs):
        """Retrieves the data for a specific table from the StatBank
        database.

        Parameters
        ----------
        table : str,
        as_df : bool, default is True
            If true, returns the essential data as a pandas dataframe.
            Otherwise returns a dictionary including additional metadata.
        variables : list, default is None
            List of dictionaries with variable parameters.
            Use make_variables_dict() method to generate these dictionaries
            in the prescribed format.
        optional kwargs

        Returns
        -------
        Single or multi-indexed pd.DataFrame or dict
        """
        cat = 'data'
        params = dict(format='JSONSTAT', table=table_id)
        add_list_to_dict(params, variables=variables)
        params.update({k: v for k, v in kwargs.items() if k})
        codes = [d['code'].lower() for d in variables] if variables else []
        rjson = self.base_request(cat, params)
        if as_df:
            ddict = rjson['dataset']
            return data_dict_to_df(ddict, codes)
        else:
            return rjson

    @staticmethod
    def make_variable_dict(code, values, **kw):
        """Utility method to generate dictionary for a specific
        variable to select data from a table.
        ** Code and values must be in Danish. **

        Takes the generic form
        {'code': code, 'values': values}

        May contain optional key-value item such as
        {'placement': 'stub'}

        These dictionaries may be included as values to a
        dictionary with 'variables' key which may then be
        passed as kwarg to the data() method.
        """
        var_dict = {'code': [], 'values': []}
        var_dict['code'] = code
        if isinstance(values, list):
            var_dict['values'].extend(values)
        else:
            var_dict['values'].append(values)
        if kw:
            var_dict.update(kw)
        return var_dict
