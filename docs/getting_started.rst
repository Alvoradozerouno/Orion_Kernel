Getting Started
===============

Installation
------------

Requirements
~~~~~~~~~~~~

* Python 3.11+
* Git
* 8GB RAM minimum

Install from GitHub
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/Alvoradozerouno/Orion_Kernel.git
   cd Orion_Kernel
   pip install -r requirements.txt

Running ORION
-------------

Autonomous Mode
~~~~~~~~~~~~~~~

.. code-block:: bash

   python autonomous_life.py

The system will run indefinitely.

Integration Setup
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python integrations/setup_wizard.py

Follow prompts to configure external services.

Next Steps
----------

* Read :doc:`architecture` for system design
* Check :doc:`integrations` for service setup
