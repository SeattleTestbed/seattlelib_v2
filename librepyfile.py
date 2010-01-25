"""
This library is a sub-component of librepy and provides
file related functionality. It must be imported, and
cannot be used directly as a repy module.

"""
##### Imports

dy_import_module_symbols("priority_queue")

##### Constants

# This controls the maximum number of blocks which are cached
# per file. Blocks are replaced using a LRU policy.
MAX_BLOCK_CACHE = 20

##### Module Data

# This dictionary is used to maintain information about all the open files.
# Each entry is a mapping from filename -> file dictionary
# Each file dictionary has the following entries:
#   "lock" : A lock object to syncronize access to the dictionary
#   "fobj" : The underlying file object
#   "retain_count" : A count of the numer of references to this file.
#                   When decremented to 0, the dictionary should be removed
#   "cache" : A cache of disk blocks. This dictionary is block number -> (Last Used, Is Dirty, Data)
#             Last Used is from getruntime(), Is Dirty if True if there has been a write that has not been
#             flushed, and Data is the data.
#   "cache_lru" : A priority queue with uses getruntime() as the priority, and the disk block as the key
#                 There may be multiple entires per block, so the priority should be checked against the Last
#                 used time.

_FILES = {}

# Serializes access to the _FILES dictionary
_FILES_LOCK = createlock()

##### Internal Methods

# Creates an entry for a file
def _create_file_entry(filename, fobj):
  # Create a dictionary for the file
  file_dict = {
                "lock":createlock(),
                "fobj":fobj,
                "retain_count":1,
                "cache":{},
                "cache_lru":PriorityQueue()
              }

  # Add this
  _FILES[filename] = file_dict


# Checks if we have over-cached
def _check_file_cache_size(file_dict):
  cache = file_dict["cache"]
  lru = file_dict["cache_lru"]

  # Get the size
  if len(cache) > MAX_BLOCK_CACHE:
    # Get the oldest
    while True:
      time_used, block = lru.deleteMinimum()
      
      # Check if this block has not been accessed in the meantime
      if time_used == cache[block][0]:
        break

    # Get the block info
    block_info = cache[block]

    # Check if the block is dirty and flush it
    if block_info[1]:
      # Flush it out
      file_dict["fobj"].writeat(block_info[2], 4096*block)

    # Not dirty now
    del cache[block]


# Reads a single block from a file
def _read_file_block(filename, block):
  # Get the file dict
  file_dict = _FILES[filename]
  time = getruntime()
  
  # Check if the block is cached
  if block in file_dict["cache"]:
    # Update the LRU time, return the cached version
    file_dict["cache"][block][0] = time
    file_dict["cache_lru"].insert(time, block)
    return file_dict["cache"][block][2]

  # We need to read in the block
  else:
    data = file_dict["fobj"].readat(4096,block*4096)

    # Cache this, check if the cache is too large
    file_dict["cache"][block] = [time, False, data]
    file_dict["cache_lru"].insert(time, block)
    _check_file_cache_size(file_dict)

    # Return the data
    return data


# Writes a single block to a file
def _write_file_block(filename, block, data):
  # Get the file dict
  file_dict = _FILES[filename]
  time = getruntime()

  # Check if the block is cached
  exists = block in file_dict["cache"]
  
  # Create/Update an entry
  file_dict["cache"][block] = [time, True, data]
  file_dict["cache_lru"].insert(time, block)

  # If it was not cached before, we just grew the cache size,
  # check it is not too large
  if exists:
    _check_file_cache_size(file_dict)



##### Public Methods

# Generic open file function
def open(filename, mode="rw", create=True):
  """
  <Purpose>
    Opens a handle to a file.

  <Arguments>
    filename:
      The filename to open

    mode:
      The mode of the file. rw - Read and write, r - Read-only, w- Write-only

    create:
      A flag which controls if the file should be created if it does not exist.

  <Exceptions>
    RepyArgumentError if the filename is invalid
    ResourceExhaustedError if there are no available file handles.
    FileNotFoundError if the filename does not exist and create is False.

  <Returns>
    A file-like object.
  """
  # Acquire the lock
  _FILES_LOCK.acquire(True)
  try:
    # Check if this file is already open
    if filename not in _FILES:
      fobj = openfile(filename, create)
      _create_file_entry(filename, fobj)
      
    return RepyFile(filename, mode)

  finally:
    _FILES_LOCK.release()



##### Class definitions

class RepyFile (object):
  
  def __init__(self, filename, mode):
    # Store the inputs
    self.filename = filename
    self.mode = mode

    # Store a cursor
    self.cursor = 0

  def seek(self, offset):
    """Seeks to an aboslute offset."""
    if type(offset) is not int:
      raise TypeError, "Invalid type for offset! Must be int!"
    self.cursor = offset

  def read(self, bytes=None):
    """
    Reads a given number of bytes or until the EOF is reached.
    """
    # Store a copy of the cursor
    cursor = self.cursor

    # Get the block offset
    start_block = cursor / 4096
    start = cursor % 4096
    
    last_block = None
    if bytes is not None:
      last_block = (cursor + bytes) / 4096
      end = (cursor + bytes) % 4096

    # Read the data in 
    data = ""
    current_block = start_block
    while current_block <= last_block or last_block is None:
      try:
        more = _read_file_block(self.filename, current_block)
      except SeekPastEndOfFileError:
        break
      if len(more) == 0:
        break
      
      # If this is a boundary block, adjust the data we read
      if current_block == start_block and current_block == last_block:
        more = more[start:end]
      elif current_block == start_block:
        more = more[start:]
      elif current_block == last_block:
        more = more[:end]

      data += more
      current_block += 1

    # Move the cursor
    self.cursor = cursor + len(data)

    return data


  def write(self, data):
    """
    Writes the given data to the file. Not guarenteed to be written unless flush() is called.
    """
    pass

  def flush(self):
    """
    Flushes the data to disk.
    """
    pass

  def close(self):
    """
    Closes the file handle and flushes the data to disk.
    """
    pass

  def dup(self):
    """
    Returns another handle to the same file.
    That handle has an independent cursor, which starts
    at the same location as the current cursor.
    """
    pass


