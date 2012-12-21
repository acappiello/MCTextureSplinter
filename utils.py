import sys

def raise_error (msg):
    """Handle when things go wrong in some reasonable way.
    For now, abort."""
    print "Error: " + msg
    sys.exit(1)
