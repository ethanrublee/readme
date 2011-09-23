readme
======

A readme follower... Its a build system that reads your readme, and tries
to do exactly what you say.

source
^^^^^^

You can get a readonly copy of this project by typing the following::
   
   git clone git://github.com/ethanrublee/readme.git

Feel free to submit patches or feature requests here: https://github.com/ethanrublee/readme

dependencies
^^^^^^^^^^^^
My dependencies are definition list.

- Python
   2.7 is preferred, as it uses argparse

Possibly others that I forgot.

build
^^^^^
Nothing to do here move along...

use
^^^
Try::

   cd readme
   ./readme.py --workspace=playing_around readme.rst

or::

   cd readme
   ./readme.py test_readme.rst

readme format
^^^^^^^^^^^^^
While this is still evolving, readme expects sections with names:

- source
   Where to get the source from
- dependencies
   What are the code dependences?
- build
   How the heck do i build it?
- test
   Shouldn't there be some tests?
- install
   How do i do a system install?
 
All of these sections are assumed to have literal blocks which may be directly
copy pasted into a terminal, with the exception begin dependencies.
 
Dependencies should contain a bulleted list, where each item is a definition list
e.g::

  - Boost
      Where to get boost...
  - OpenCV
      You should use version 2.3 or greater
 
Literal blocks will be run in a shell session and should only contain valid
shell code.

todo
^^^^

- add support for uri's of readmes
- **handle dependencies**
- allow for installing to different locations
- packaging debians out of anything that is installed


references
^^^^^^^^^^

http://docutils.sourceforge.net/docs/user/rst/quickref.html
http://docutils.sourceforge.net/docs/user/links.html
