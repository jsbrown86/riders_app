"""
CONFIG module
We put here things that we might vary
depending on which machine we are running
on, or whether we are in debugging mode, etc.
"""
COOKIE_KEY = "A random string would be better"
DEBUG = False
PORT = random.randit(5000,8000)  # The default Flask port; change for shared server machines


