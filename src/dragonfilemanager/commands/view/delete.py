#!/usr/bin/env python

import dragonFM
import os, shutil

# Get the files and directories that were selected.
selected = selectionManager.getSelectionOrCursorCurrentTab()

# Loop through the files and directories and delete them.
for i in selected:
    if os.is_file(i):
        os.remove(i)
    if os.is_dir(i):
        shutil.rmtree(i)


