External Integrations
=====================

ORION integrates with 6 external services for maximum visibility.

Phase 1: High Priority
-----------------------

Zenodo
~~~~~~

Dataset publishing with DOI generation.

Setup:

.. code-block:: bash

   python integrations/setup_wizard.py

Select option 1 (Zenodo).

LinkedIn
~~~~~~~~

Professional networking and research announcements.

Twitter/X
~~~~~~~~~

Real-time updates to AI community.

Phase 2: Medium Priority
-------------------------

HuggingFace
~~~~~~~~~~~

AI model and dataset hosting, Spaces for dashboards.

arXiv
~~~~~

Academic paper submission preparation.

ReadTheDocs
~~~~~~~~~~~

Professional documentation hosting (you are here!).

Management
----------

Unified CLI:

.. code-block:: bash

   python integrations/integration_manager.py --check

Announce milestone:

.. code-block:: bash

   python integrations/integration_manager.py --announce "Milestone" --phi 0.74

Full documentation: integrations/README.md in repository
