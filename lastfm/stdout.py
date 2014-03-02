# import this instead of xchat to print to stdout

EAT_ALL=None

command=print

def hook_command(dummy, hook, help=None):
	hook(None, None, None)