#!/usr/bin/python3
import cgi

def get_cmd():
  args = cgi.FieldStorage()
  cmd = args['cmd'].value
  return cmd

cmd = get_cmd()
state = " ".join(cmd.split('_'))
print("Content-Type: text/html\n")
print(f"<html> <head> <center><h1>{state} Covid-19 Data</h1></center> </head>")
print("<body>")
# Change this variable with your username
print(f'<li><a href="../index.html">Go back to home page</a></li>')
print(f'<img src="make_fig.py?cmd={cmd}">')
#print(f'<img style="position:absolute; clip: rect(100, 1000px, 1000px, 0);" "src="make_fig.py?cmd={cmd}">')
print("</body></html>")
