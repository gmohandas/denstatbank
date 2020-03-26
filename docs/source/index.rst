.. denstatbank documentation master file, created by
   sphinx-quickstart on Tue Mar 24 12:48:52 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to denstatbank's documentation!
=======================================

denstatbank is a python wrapper to Statistics Denmark's Databank API.
The package allows you to easily gather data on a variety of topics made 
available by Statistics Denmark.

Quick Start
===========

Let us walkthrough a quick example of how to query for data on a specific
topic. In this example, we shall look at population data for Denmark. 

.. code-block:: python

   >>> from denstatbank import StatBankClient
   >>> sbc = StatBankClient(lang='en')
   

Let's find a table to get data from the databank. 

.. code-block:: python

   >>> tdf = sbc.tables()
   >>> tdf.iloc[0]
   id                                                  FOLK1A
   text            Population at the first day of the quarter
   unit                                                number
   updated                                2020-02-11T08:00:00
   firstPeriod                                         2008Q1
   latestPeriod                                        2020Q1
   active                                                True
   variables         [region, sex, age, marital status, time]


| Great! Now let's extract a subset of variable values to query data.
| In this case, we get all the time periods for which data is available.
| One way to do that is as shown below

.. code-block:: python

   >>> vdf = sbc.tableinfo('folk1a', variables_df=True)
   >>> years = vdf[vdf['variable']=='time']['id'].tolist()

| Now, let's query for the actual population data.
| But first, we need to make a variable dictionary as follows

.. code-block:: python

   >>> tid = sbc.variable_dict(code='tid', values=years)

| Note: The variable key codes must be specified in Danish. In this case, 'tid' for time. 
| Now, let's get the data into a pandas dataframe.

.. code-block:: python

   >>> df = sbc.data(table_id='folk1a', variables=[tid])
   >>> df.head()
              Population at the first day of the quarter by Indhold and time
   tid                                                                   
   2008Q1                                            5475791             
   2008Q2                                            5482266             
   2008Q3                                            5489022             
   2008Q4                                            5505995             
   2009Q1                                            5511451


| We utilize the pandas library in python which comes along part of the installation.
| Pandas is a fast and powerful library well suited for data handling and analysis in python. 

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   denstatbank.denstatbank
   denstatbank.utils

   

.. :caption: Contents:

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
