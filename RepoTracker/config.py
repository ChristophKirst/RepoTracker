"""
ReproTracker 
============

Configuration file.
"""
__author__    = 'Christoph Kirst <christoph.kirst.ck@gmail.com>'
__copyright__ = 'Copyright (c) by Christoph Kirst'
__license__   = 'GPL v3'


user = "ChristophKirst";
"""Username for the repository to track"""

repos = ["ClearMap", 
         "RepoTracker"];
"""List of repository names to track"""


statistics = {"traffic/views": "timestamps",
              "traffic/clones": "timestamps", 
              "traffic/popular/referrers":  "records", 
              "traffic/popular/paths": "records"};
"""Dictionary of the form {"statistic" : "method"}"""
