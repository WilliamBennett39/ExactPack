Release Notes for ExactPack
===========================

Version 1.7.0 (Dec 2022)
------------------------

* Convert all code the be compatible with Python 3
* Removed all Fortran Code. Extant Fortran solvers have been converted to Python where necessary
* Removed all code associated with the GUI, CLI and verification analysis
* Added solver for the Radshocks problem
* Added general solver for the Riemann problems
* Added solver the Elastic-Plastic Piston problem
* Switched all tests to using Pytest

Version 1.6.0 (Aug 2017)
-------------------------

* Added solver for Uniform Collapse problem (a.k.a. Noh2, Shockless Noh)
* Added solvers for heat conduction problems
* Added additional methods to fit convergence rate, and refactored verification analysis syntax

Version 1.5.3 (Mar 2017)
-------------------------

* Cleaned up variable names and formatting
* Fixed error in test_riemann.py that prevented some tests from being discovered

Version 1.5.2 (Feb 2017)
-------------------------

* Changed recommended installation method for ExactPack from conda install to "build from source"
* Noted that NumPy 1.12.0 is not compatible with ExactPack
* Changed Jenkins script to specify NumPy version 1.11.3
* Deleted an extraneous file in the Noh solver directory

Version 1.5.1 (Jan 2017)
-------------------------

* Updated credits.rst

Version 1.5.0 (Jan 2017)
-------------------------

* Added native Python solver for Sedov, called the Doebling solver.
* Added support for the Jenkins automated build and test software
* Updated github path to reflect renaming of 'losalamos' project to 'lanl'

Version 1.4.1 (Nov 2016)
-------------------------

* Fixed a bug in the Blake solver that was dependent upon Python version

Version 1.4.0 (Sept 2016)
-------------------------

* Added three test problem solvers for the Detonation Shock Dynamics model (rate stick,
cylindrical expansion, explosive arc). These solvers have not been thoroughly
tested and should be considered beta.
* Improved error checking for Coggeshall solvers
* Corrected some documentation errors


Version 1.3.0 (Apr 2016)
------------------------

* Initial release of ExactPack as Open Source Software
