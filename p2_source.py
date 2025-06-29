import sqlite3
import pandas as pd
import numpy as np
from lets_plot import *

LetsPlot.setup_html(isolated_frame=True)

sqlite_file = "lahmansbaseballdb.sqlite"
# this file must be in the same location as your .qmd or .py file
con = sqlite3.connect(sqlite_file)
