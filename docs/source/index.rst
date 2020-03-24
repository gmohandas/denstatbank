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

.. code-block:: python

   >>> from denstatbank import StatBankClient
   >>> sbc = StatBankClient(lang='en')
   >>> sbc.subjects()



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
