import sys

if sys.version_info < (2, 7):
    import commands
else:
    import subprocess


def commands_getoutput(cmd):
    try:
        if sys.version_info < (2, 7):
            return commands.getoutput(cmd)
        else:
            byte_out = subprocess.check_output(cmd.split())
            str_out = byte_out.decode("utf-8")
            return str_out
    except Exception as e:
        return str(e)
