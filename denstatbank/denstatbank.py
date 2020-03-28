import requests
import pandas as pd
from urllib.parse import quote
from .utils import data_dict_to_df, add_list_to_dict, subtabtree


class StatBankClient:
    """Client that connects to the Databank API of Statistics Denmark.

    Attributes
    ----------
    lang : str, {'da', 'en'} default is 'da'
        Note: Variable key codes to be passed when requesting specific data
        must be in Danish. Please see data() method docstring for details. 
        As long as Danish key codes are provided as input, one can use the 
        Class with English language settings.
    """

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
            raise ValueError(
                'Language can only accept either "en" or "da" as values.')
        self._lang = value

    def _base_request(self, cat, params):
        """
        Submits all POST request to API and returns response.
        Used internally by all client facing methods.
        """
        params.update({'lang': self.lang})
        try:
            resp = self.session.post(self._base_url+quote(cat), json=params)
            if resp.status_code == 200:
                return resp.json()
            else:
                response_message = resp.json()['message']
                print(response_message)
        except Exception as ex:
            raise ex

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

        Examples
        --------
        >>> sbc.subjects(['19'], recursive=True)
                 |--('19', 'Other')
                 |       |--('2473', 'Statistisk Årbog')
                 |       |--('2472', 'Statistisk Tiårsoversigt')
                 |       |--('2475', 'Danmark i Tal')
                 |       |--('2474', 'Nordic Statistical Yearbook')
                 |       |--('2483', 'Publications')
                 |       |       |--('10392', 'Generel publications')
                 |       |       |--('10393', 'Methodology')
                 |       |       |--('10394', 'Nomenclatures and classifications')
                 |       |--('2482', 'Municipal service indicators')
                 |       |       |--('10376', 'Elderly care')
                 |       |       |--('10378', 'Disadvantaged children and young people')
                 |       |       |--('10377', 'Health')ss
        """
        cat = 'subjects'
        params = dict(includeTables=include_tables, recursive=recursive)
        add_list_to_dict(params, subjects=subjects)
        resp = self._base_request(cat, params)
        if resp is not None:
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

        Examples
        --------
        >>> df = sbc.tables()
        >>> df.iloc[0]
        id                                                  FOLK1A
        text            Population at the first day of the quarter
        unit                                                number
        updated                                2020-02-11T08:00:00
        firstPeriod                                         2008Q1
        latestPeriod                                        2020Q1
        active                                                True
        variables         [region, sex, age, marital status, time]
        Name: 0, dtype: object

        >>> df.shape
        (2116, 8)
        """
        cat = 'tables'
        params = dict(pastdays=past_days, includeinactive=include_inactive)
        add_list_to_dict(params, subjects=subjects)
        resp = self._base_request(cat, params)
        if as_df and resp is not None:
            return pd.DataFrame(resp)
        else:
            return resp

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

        Examples
        --------
        >>> vdf = sbc.tableinfo(table_id='bef5', variables_df=True)
        >>> vdf.head()
          id     text variable
        0  M     Mænd      KØN
        1  K  Kvinder      KØN
        0  0     0 år    ALDER
        1  1     1 år    ALDER
        2  2     2 år    ALDER
        """
        cat = 'tableinfo'
        params = dict(table=table_id)
        resp = self._base_request(cat, params)
        if resp is not None:
            if variables_df:
                var_df = pd.DataFrame()
                varlist = resp['variables']
                for d in varlist:
                    df = pd.DataFrame(d['values'])
                    if params['lang'] == 'en':
                        df['variable'] = d['text']
                    else:
                        df['variable'] = d['id']
                    var_df = var_df.append(df)
                return var_df
            else:
                return resp

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

        Examples
        --------
        >>> sbc.data(table_id='folk1a')
                Folketal den 1. i kvartalet efter Indhold og tid
            0                                           5822763

        >>> kon = sbc.variable_dict(code='KØN', values=['M', 'K'])
        >>> tid = sbc.variable_dict(code='Tid', values=['2018'])
        >>> df = sbc.data(table_id='bef5', variables=[tid, kon])
        >>> df
                    Population 1. January by sex, Indhold and time
        køn   tid
        Men   2018                                         2876473
        Women 2018                                         2904717
        """
        cat = 'data'
        params = dict(format='JSONSTAT', table=table_id)
        add_list_to_dict(params, variables=variables)
        params.update({k: v for k, v in kwargs.items() if k})
        codes = [d['code'].lower() for d in variables] if variables else []
        resp = self._base_request(cat, params)
        if as_df and resp is not None:
            ddict = resp['dataset']
            return data_dict_to_df(ddict, codes)
        else:
            return resp

    @staticmethod
    def variable_dict(code, values, **kw):
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

        Examples
        --------
        >>> tid = sbc.variable_dict('Tid', ['2018', '2019'])
        >>> tid
        {'code': 'Tid', 'values': ['2018', '2019']}
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
