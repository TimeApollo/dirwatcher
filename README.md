# DIRWATCHER Program

This Program watches specified directory for magic text in
files with a specified extension. The program checks based on
time specified or the default value of 1 sec.

All information is logged to the stdout and a log file called dirwatch.log.
Information that is logged is start time, occurrences of the magic text, stop duration,
and any errors that occur as it runs.

The point of the program is to keep running even if there are errors.
The only time it ends its running is if a SIGTERM or SIGINT is sent. It will try to
continue to run through all other errors or signals if it can.

#### CMD Help ####

usage: dirwatcher.py [-h] [-i INT] [-d DIR] [-t TEXT] [-e EXT]

Dirwatcher Arguments

optional arguments:
  -h, --help            show this help message and exit
  -i INT, --int INT     Polling interval for program.(sec) (Default=1)
  -d DIR, --dir DIR     Directory to search for files. (Default=./)
  -t TEXT, --text TEXT  Magic text to search for in files. (Default=magic)
  -e EXT, --ext EXT     File extension of file to search through.
                        (Default=txt)


All arguments are optional.