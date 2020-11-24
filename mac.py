import subprocess

# stolen from https://github.com/asweigart/pyperclip/blob/master/src/pyperclip/__init__.py


def copy_to_clipboard(value: str):
    p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=value.encode('utf-8'))
