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
            byte_out = subprocess.check_output(cmd)
            str_out = byte_out.decode("utf-8")
            return str_out
    except Exception as e:
        return str(e)


def map_number(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
