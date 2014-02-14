"""
<Filename>
  ut_seattlelib_parallelize_finishes.py

<Purpose>
  Verifies that parallelize marks a job as finished when all its
  arguments are processed, and all threads started by a particular
  handle terminate.  See #1306.

"""

from repyportability import *
add_dy_support(locals())
dy_import_module_symbols('parallelize.repy')


# Maximum amount of time we're allowing the parallel thread calls to
# finish.  If the callback we pass to parallelize is the null function,
# 5 seconds should be plenty for even a large amount of arguments.
MAX_ELAPSED_TIME = 5

# This number should be high compared to the number of parallel threads
# we'll start via parallelize_initfunction().
DUMMY_THREADS = 50


def infinite_loop():
  while True:
    pass

def void_function(value):
    pass

def main():
  # We want to delay parallelize's threads as much as possible, so let's
  # introduce some thread contention
  for i in xrange(DUMMY_THREADS):
    createthread(infinite_loop)

  some_arguments = range(20)
  handle = parallelize_initfunction(some_arguments, void_function)

  starttime = getruntime()
  while not parallelize_isfunctionfinished(handle):
    if getruntime() - starttime > MAX_ELAPSED_TIME:
      print "Did not finish running in a timely manner!"
      break
    sleep(0.1)

  # If we don't explicitly exit, the dummy threads will cause the test to
  # hang forever as repy exits when all threads are finished.
  exitall()


main()
