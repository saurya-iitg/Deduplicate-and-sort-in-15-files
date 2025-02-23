#!/usr/bin/env python3
#
#  sort-in15-files-chunk.py
#  
#  Copyright 2024 saura <saura@VD>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os

def sort_files_in_chunks(directory, chunk_size=15):
  """Sorts files in the given directory by name and moves them to subfolders
  in chunks of chunk_size.

  Args:
      directory: The directory containing the files to sort.
      chunk_size: The number of files to move to each subfolder (default: 15).
  """

  # Get a list of files in the directory, sorted by name
  files = os.listdir(directory)
  files.sort()

  # Create subfolders with names indicating file count range
  folder_num = 1
  for i in range(0, len(files), chunk_size):
    folder_name = f"folder{folder_num}"
    os.makedirs(os.path.join(directory, folder_name), exist_ok=True)

    # Move files in the current chunk to the subfolder
    for filename in files[i:i+chunk_size]:
      source = os.path.join(directory, filename)
      destination = os.path.join(directory, folder_name, filename)
      os.rename(source, destination)

    folder_num += 1

if __name__ == "__main__":
  # Get the current working directory
  directory = os.getcwd()

  # Sort files in the current directory
  sort_files_in_chunks(directory)

  print("Files sorted and moved to subfolders successfully!")
