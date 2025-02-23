#!/usr/bin/env python3
#
#  untitled.py
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
import hashlib
from shutil import copy2

def sort_and_deduplicate(source_dir, copy_source_dir, copy_conflict_dir, folder_size):
    """
    Sorts files by size, checks for duplicates using size and hash,
    organizes files into folders, and handles conflicts.

    Args:
        source_dir (str): Path to the directory containing files to sort.
        copy_source_dir (str): Path to the directory for storing single copies.
        copy_conflict_dir (str): Path to the directory for storing conflicts.
        folder_size (int): Number of files per folder.
    """

    # Create directories if they don't exist
    os.makedirs(copy_source_dir, exist_ok=True)
    os.makedirs(copy_conflict_dir, exist_ok=True)

    # Dictionary to store size as key and a list of (filename, hash) tuples as value
    file_data = {}
    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        if os.path.isfile(filepath):
            file_size = os.path.getsize(filepath)
            with open(filepath, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            if file_size not in file_data:
                file_data[file_size] = []
            file_data[file_size].append((filename, file_hash))

    # Sort file data by size (ascending)
    sorted_data = sorted(file_data.items())

    folder_num = 1  # Track folder number for organization
    current_folder = os.path.join(source_dir, f"folder{folder_num}")
    file_count = 0  # Track number of files in current folder

    for size, file_list in sorted_data:
        # Check for duplicates within same size group
        seen_hashes = set()
        for filename, file_hash in file_list:
            if file_hash in seen_hashes:
                # Duplicate found, move both files to conflict directory
                conflict_source = os.path.join(source_dir, filename)
                conflict_dest = os.path.join(copy_conflict_dir, filename)
                copy2(conflict_source, conflict_dest)

                existing_conflict = os.path.join(copy_conflict_dir, os.path.basename(conflict_source))
                if os.path.exists(existing_conflict):
                    # Generate unique filename for conflict by appending a number
                    conflict_num = 1
                    conflict_base, conflict_ext = os.path.splitext(existing_conflict)
                    while os.path.exists(f"{conflict_base}{conflict_num}{conflict_ext}"):
                        conflict_num += 1
                    conflict_dest = f"{conflict_base}{conflict_num}{conflict_ext}"
                    copy2(conflict_source, conflict_dest)
                    print(f"Conflict: {filename} (original moved to {conflict_dest})")
                else:
                    print(f"Conflict: {filename}")

            else:
                # No duplicate, move file to source or create new folder if full
                if file_count < folder_size:
                    source_dest = os.path.join(current_folder, filename)
                    copy2(os.path.join(source_dir, filename), source_dest)
                    file_count += 1
                else:
                    folder_num += 1
                    current_folder = os.path.join(source_dir, f"folder{folder_num}")
                    file_count = 1
                    source_dest = os.path.join(current_folder, filename)
                    copy2(os.path.join(source_dir, filename), source_dest)
                seen_hashes.add(file_hash)

if __name__ == "__main__":
    source_dir = "C:\\Wondershare\\KwiCut\\Output\\temp"  # Replace with your actual directory path
    copy_source_dir = "copy_source"  # Directory to store single copies
    copy_conflict_dir = "copy_conflict"  # Directory to store conflicts
    folder_size = 15  # Number of files
