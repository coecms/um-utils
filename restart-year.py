#!/usr/bin/env python
"""
file:   restart-year
author: Scott Wales <scott.wales@unimelb.edu.au>

Copyright 2013 ARC Centre of Excellence for Climate System Science

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

--------------------------------------------------------------------------------

Print the year that a run will be restarted at

Search the $RUNID.phist file for 'END_DUMPIM' entries, the first will be the
most recent

This will give a UM-style filename for the last dump file the run wrote
(similarly ASTART gives the first, however for the first segment we get
$RUNID.astart instead of a timestamped filename.

Use like:
   ./restart-year.py $RUNID.phist
to get '1950' on stdout

"""

def decode_year(code):
    """
    Gets the year from a UM timestamp
    """
    try:
        decade = int(code[0])
    except ValueError:
        decade = 10 + ord(code[0]) - ord('a')
    year = int(code[1])
    return decade * 10 + year + 1800


import fileinput
import re

# Match END_DUMPIM lines & extract the filename:
# END_DUMPIM      = 'uaknba_da024  ', 3*'              ',
dumpline = re.compile(r'\s*END_DUMPIM\s+=\s*\'(\S+)\s*\',.*')

for line in fileinput.input():
    line = line.strip()

    matches = dumpline.match(line)
    if matches:
        final_dump = matches.group(1)
        break

if final_dump[6] != '.':
    print "Wrong filename convention"
    exit(-1)

year = decode_year(final_dump[9:])
print year

