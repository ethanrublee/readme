image_pipeline
==============
Core C++ functionality for image_pipeline.

 * Camera Models
 * Calibration routines including writing and reading from disk
 * Camera interface conventions
 * Project routines
 * Rectification routines

Also has plugs for:
 * ROS
 * ecto

source
^^^^^^

We use git as our repository::
   
   git clone git://github.com/wg-perception/image_pipeline.git

dependencies
^^^^^^^^^^^^
My dependencies are definition list.

- Boost
   Anything over 1.40 http://www.boost.org
- OpenCV
   version >= 2.3 http://opencv.willowgarage.com
- Eigen
   version >= 3.0 http://eigen.tuxfamily.org
- gtest
   http://code.google.com/p/googletest


build
^^^^^
This is how you should build the image_pipeline::

   cd image_pipeline
   mkdir build
   cd build
   cmake .. -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX
   make

test
^^^^
To run our amazing tests::

   cd image_pipeline/build
   make
   ctest -V

install
^^^^^^^
If you wish to install image_pipeline just run::

   cd image_pipeline/build
   make install

use
^^^
See samples/user_project for a project that uses image_pipeline

