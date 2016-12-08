Weeman - http server for phishing
==================================

News
=====

* Added profiles
* Weeman framework 0.1 is out !!!
* Added command line options.
* Beautifulsoup dependency removed.

About
=====

HTTP server for phishing in python. (and framework)
Usually you will want to run Weeman with DNS spoof attack. (see dsniff, ettercap).

![Weeman](https://raw.githubusercontent.com/Hypsurus/weeman/master/core/weeman_curr.png)


Weeman will do the following steps:
------------------------------------

1. Create fake html page.
2. Wait for clients
3. Grab the data (POST).
4. Try to login the client to the original page :smiley:

The framework
---------------

You can use weeman with modules see examples in `modules/`,
just run the command `framework` to access the framework.

#### Write a module for the framework

If you want to write a module please read the modules/.
Soon I will write docs for the API.

Tools
======

* tools/weeman_ettercap.sh - run ettercap with dns_spoof plugin.

Profiles
=========

You can load profiles in weeman, for example profile for mobile site and profile for desktop site.

`./weeman.py -p mobile.localhost.profile`

Requirements
============

* Python <= 2.7.

Platforms
-----------

* Linux (any)
* Mac (Tested)
* Windows (Not supported)

Contributing
=============

Contributions are very welcome!

1. fork the repository
2. clone the repo (git clone git@github.com:USERNAME/weeman.git)
3. make your changes
6. Add yourself in contributors.txt
4. push the repository
5. make a pull request

Thank you - and happy contributing!

DISCLAIMER
==========

Usage of Weeman for attacking targets without prior mutual consent is illegal.
Weeman developer not responsible to any damage caused by Weeman.

Copying
========

###### Copyright 2015 (C) Hypsurus <hypsurus@mail.ru>
###### License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
###### [Beautifulsoup 4 library](http://www.crummy.com/software/BeautifulSoup/bs4/) by Leonard Richardson under the MIT license.
