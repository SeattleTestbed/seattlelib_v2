"""
This library is a sub-component of librepy and provides
file related functionality. It must be imported, and
cannot be used directly as a repy module.

"""
##### Imports


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
#   "size"  : Size of the file. This is computed once, and then updated based on writes

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
                "retain_count":0,
                "cache":{},
                "size":None,
              }

  # Add this
  _FILES[filename] = file_dict

  # Set the file size
  file_dict["size"] = _probe_file_size(filename)


# Increments the reference count of a file
def _inc_file_refcount(filename):
    # Increment the retain count
    file_dict = _FILES[filename]
    file_dict["lock"].acquire(True)
    file_dict["retain_count"] += 1
    file_dict["lock"].release()


# Checks if we have over-cached
def _check_file_cache_size(file_dict):
  cache = file_dict["cache"]

  # Get the size
  if len(cache) > MAX_BLOCK_CACHE:
    # Get the oldest, store (block #, Block Info)
    min_block = None

    for block, block_info in cache.items():
      if min_block is None or min_block[1][0] > block_info[0]:
        min_block = (block, block_info)

    # Check if the block is dirty and flush it
    if min_block[1][1]:
      # Flush it out
      file_dict["fobj"].writeat(min_block[1][2], 4096*min_block[0])

    # Not dirty now
    del cache[min_block[0]]


# Reads a single block from a file
def _read_file_block(filename, block):
  # Get the file dict
  file_dict = _FILES[filename]
  file_dict["lock"].acquire(True)
 
  try:
    # Check if the block is cached
    if block in file_dict["cache"]:
      # Update the LRU time, return the cached version
      file_dict["cache"][block][0] = getruntime()
      return file_dict["cache"][block][2]

    # We need to read in the block
    else:
      data = file_dict["fobj"].readat(4096,block*4096)

      # Cache this, check if the cache is too large
      file_dict["cache"][block] = [getruntime(), False, data]
      _check_file_cache_size(file_dict)

      # Return the data
      return data

  finally:
    # Release the lock
    file_dict["lock"].release()


# Writes a single block to a file
def _write_file_block(filename, block, data):
  # Get the file dict
  file_dict = _FILES[filename]
  file_dict["lock"].acquire(True)

  try:
    # Check if the block is cached
    cached = block in file_dict["cache"]
  
    # Check if the data is different
    changed = True
    if cached:
      changed = data != file_dict["cache"][block][2]

    # Check if this is the last block
    last_block = file_dict["size"] / 4096
    if block == last_block:
      # Update the file size
      file_dict["size"] = 4096*block + len(data)

    # Create/Update an entry
    file_dict["cache"][block] = [getruntime(), changed, data]

    # If it was not cached before, we just grew the cache size,
    # check it is not too large
    if not cached:
      _check_file_cache_size(file_dict)

  finally:
    # Release the lock
    file_dict["lock"].release()


# Binary probe to find the file size
def _probe_file_size(filename):
  """Returns the size of the file in bytes."""
  low_block = 0
  high_block = 1
  max_hit = False

  # Get a rough bounds on the size first
  while low_block < high_block:
    current_block = low_block + (high_block - low_block) / 2
    try:
      block_data = _read_file_block(filename, current_block)
      good_block = current_block # Store the last 'good' block
      low_block = current_block
      if not max_hit:
        high_block = high_block * 2 
      else:
        low_block += 1

    except SeekPastEndOfFileError:
      high_block = current_block - 1
      max_hit = True

  return 4096*good_block + len(block_data)



##### Public Methods

# Generic open file function
def open(filename, mode="rw", create=True):
  """
  <Purpose>
    Opens a handle to a file. If you open a handle to a file which
    is already open, you will get an independent handle, with it's own
    cursor.

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
    if filename not in _FILES:
      raise RepyArgumentError, "Do not initialize the RepyFile object directly! Use open()"
    
    # Increment the retain count
    _inc_file_refcount(filename) 

    # Store the inputs
    self.filename = filename
    self.mode = mode

    # Store a cursor
    self.cursor = 0
    self.cursor_lock = createlock()

    # Calculate the size
    self.size()

  
  def _closed(*args, **kwargs):
    raise FileClosedError, "File is closed!"


  def tell(self):
    """Returns the current position of the cursor."""
    return self.cursor


  def seek(self, offset, fromStart=True):
    """
    Seeks to an aboslute offset.
    If fromStart is True, then offset is from the start of the file.
    If fromStart is False, then offset if from the end of the file.
    """
    if type(offset) is not int:
      raise TypeError, "Invalid type for offset! Must be int!"
    if offset < 0:
      raise ValueError, "Offset must be a non-negative value!"

    # Check the file size
    size = self.size()
    if offset > size:
      raise RepyArgumentError, "Offset exceeds the file size!"


    # Acquire the lock, update the cursor and release
    self.cursor_lock.acquire(True)

    if fromStart:
      self.cursor = offset
    else:
      self.cursor = self.size() - offset

    self.cursor_lock.release()


  def size(self):
    """Returns the size of the file in bytes."""
    # Get the file dict
    file_dict = _FILES[self.filename]
    return file_dict["size"]


  def read(self, bytes=None):
    """
    Reads a given number of bytes or until the EOF is reached.
    """
    # Check the mode
    if "r" not in self.mode:
      raise RepyArgumentError, "File opened as write-only! Cannot read!"

    # Check the bytes argument
    if bytes is not None and type(bytes) is not int:
      raise TypeError, "Bytes argument must be an integer or 'None'!"
    if bytes is not None and bytes < 0:
      raise ValueError, "Bytes must be a non-negative integer!"

    # Acquire the cursor lock
    self.cursor_lock.acquire(True)

    try:
      # Store a copy of the cursor
      cursor = self.cursor

      # Get the block offset
      start_block = cursor / 4096
      start_offset = cursor % 4096
      
      end_block = None
      if bytes is not None:
        end_block = (cursor + bytes) / 4096
        end_offset = (cursor + bytes) % 4096

      # Read the data in 
      data = ""
      current_block = start_block
      while current_block <= end_block or end_block is None:
        try:
          block_data = _read_file_block(self.filename, current_block)
        except SeekPastEndOfFileError:
          break
        if len(block_data) == 0:
          break
        
        # If this is a boundary block, adjust the data we read
        if current_block == end_block:
          block_data = block_data[:end_offset]
        if current_block == start_block:
          block_data = block_data[start_offset:]

        # Add this to the total data
        data += block_data
        current_block += 1

      # Move the cursor
      self.cursor = cursor + len(data)

      return data

    finally:
      # Release the cursor lock
      self.cursor_lock.release()


  def write(self, data):
    """
    Writes the given data to the file. Not guarenteed to be written unless flush() is called.
    """
    # Check the mode
    if "w" not in self.mode:
      raise RepyArgumentError, "File is opened as read-only! Cannot write!"

    # Check the data argument
    if type(data) is not str:
      raise TypeError, "Data must be provided as a string type!"
    if len(data) == 0:
      return

    # Acquire the cursor lock
    self.cursor_lock.acquire(True)

    try:
      # Store a copy of the cursor
      cursor = self.cursor

      # Get the block offset
      start_block = cursor / 4096
      start_offset = cursor % 4096
      
      bytes = len(data)
      end_block = (cursor + bytes) / 4096
      end_offset = (cursor + bytes) % 4096

      # If we are writing a whole block, then we are okay.
      # If we are writing a partial block, we need to read in
      # the block, and then fill it in.
      if start_offset > 0:
        block_data = _read_file_block(self.filename, start_block)
        data = block_data[:start_offset] + data
      if end_offset > 0:
        try:
          block_data = _read_file_block(self.filename, end_block)
          data = data + block_data[end_offset:]
        except SeekPastEndOfFileError:
          pass

      current_block = start_block
      while current_block <= end_block or end_block is None:
        block_data = _write_file_block(self.filename, current_block, data[:4096])
        data = data[4096:]
        current_block += 1
        
      # Move the cursor
      self.cursor = cursor + bytes

    finally:
      # Release the cursor lock
      self.cursor_lock.release()


  def flush(self):
    """
    Flushes the data to disk.
    """
    # Get the file dict
    file_dict = _FILES[self.filename]
    cache = file_dict["cache"]

    # Acquire the lock
    file_dict["lock"].acquire(True)
    try:
      # Get a list of all the dirty blocks
      dirty_blocks = []

      for block, block_info in cache.items():
        if block_info[1]:
          dirty_blocks.append(block)

      # Sort the blocks, we must flush in-order
      # to prevent seeking past the end of the file
      dirty_blocks.sort()

      # Flush it out
      for block in dirty_blocks:
        file_dict["fobj"].writeat(cache[block][2], 4096*block)
        cache[block][1] = False # Set dirty to false

    finally:
      # Release the lock
      file_dict["lock"].release()


  def close(self):
    """
    Closes the file handle and flushes the data to disk.
    """
    # Flush the dirty blocks
    self.flush()

    # Switch all the functions to the closed function
    self.tell = self._closed
    self.seek = self._closed
    self.size = self._closed
    self.read = self._closed
    self.write = self._closed
    self.flush = self._closed
    self.close = self._closed
    self.dup = self._closed

    # AGet the dictionary for this file
    file_dict = _FILES[self.filename]

    _FILES_LOCK.acquire(True)
    file_dict["lock"].acquire(True)
    try:
      # Reduce the retain count
      file_dict["retain_count"] -= 1

      # If the retain count is 0, delete the file
      if file_dict["retain_count"] == 0:
        file_dict["fobj"].close()
        del _FILES[self.filename]

    finally:
      file_dict["lock"].release()
      _FILES_LOCK.release()


  def dup(self):
    """
    Returns another handle to the same file.
    That handle has an independent cursor, which starts
    at the same location as the current cursor.
    """
    # Create another instance
    fileh_dup = RepyFile(self.filename, self.mode)

    # Seek to the current position
    fileh_dup.seek(self.cursor)

    # Return the duplicate
    return fileh_dup

  # Handle GC for implicit cleanup
  #def __del__(self):
  ##  try:
  #    self.close()
  #except:
  #  pass


