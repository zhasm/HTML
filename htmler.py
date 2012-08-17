#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# author  : Rex Zhang
# datetime: 2012-07-31 21:57:12
# filename: HTML.py
"""
HTML Table MaiLer

## an sh script example
#!/usr/bin/env bash

tmp=`mktemp`
d=`date +"%b %e"` #yesterday
to='rex@mydomain.com'
mailer='/usr/bin/python /home/rex/bin/HTML'
header="Subject Price Value Link"
header="货物 售价 原价 链接"
main="/usr/bin/python /home/rex/bin/some script.py"
title=" "
subject="商品类新单 on $d"
frm="rex@from.com"
$main > $tmp
$mailer -f "$frm" -t $to -s "$subject" --header "$header" --title "$title" < $tmp
/bin/rm -f $tmp

"""
import re

try:
    from mailer import Message, Mailer
except ImportError:
    print "Please install Python Module: `sudo pip install mailer`, or `sudo easy_install mailer` before using this script."
    exit()

class HTMLTable(object):
    def __init__(self, args):
        self.args=args

    def title(self):
        if self.args.title: return "<h3>%s</h3>" % self.args.title

    def tHeader(self):
        args=self.args
        headers=re.split(args.fs, args.header, args.max_split)
        format='''<th style="padding: 0px 10px;">%s</th>'''
        headers=[format % i for i in headers]
        return '''<thead>\n<tr align="center" style="background-color: #E6EEEE; font-family: arial; font-size: 10pt; margin: 10px ;">''' + \
               "\n" + \
                "\n".join(headers) + \
            "\n</tr>\n</thead>"

    def tBody(self):
        args=self.args
        format='''<td style="border: 1px solid #E6EEEE; padding: 0px 5px;">%s</td>'''
        ret=[]
        for line in args.lines:
            cols=re.split(args.fs, line, args.max_split)
            cols=[format % i for i in cols]
            ret.append( "<tr>" + "\n".join(cols) + "<tr/>")

        return '''<tbody style="font-size: 10pt;" align="left">''' + "\n".join(ret) + '''</tbody>'''

    def _htmlStrip(self, html):
        html=re.sub(r'\s\s+', ' ', html)

    def __str__(self):
        pre='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
          <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                  </head>
                  <body>
                  %s
                  <table class="filament" cellspacing="1" style="border-spacing: 1px; " >
                  ''' % self.title()
        post="</table></body></html>"

        html= "\n".join([pre, self.tHeader(), self.tBody(),  post])
        #trim
        html=re.sub(r'\s\s+', ' ', html)
        html=re.sub(r'<!--.*?-->', '\n', html)
        return html

def getArgs():
    """show argpase snippets"""
    import argparse

    parser = argparse.ArgumentParser()

    ##for mailer
    parser.add_argument('-H', '--host', default='localhost', help="mailer host; Gmail=smtp.gmail.com")
    parser.add_argument('-P', '--port', default=25, type=int, help="mailer port, defult 25; for gmail: TLS/STARTTLS: 587, Port for SSL: 465")
    parser.add_argument('-u', '--username', default="")
    parser.add_argument('-p', '--password', default="")

    #for Message
    parser.add_argument('-f', '--frm')
    parser.add_argument('-t', '--to')
    parser.add_argument('-s', '--subject')
    parser.add_argument('--title', help="the title for the table body", default=" ")
    parser.add_argument('--fs', default=r'\s+', help='split columns with; in r"regex" syntax; default r"\s+"')
    parser.add_argument('--max-split', default=0, type=int, help='split the first N, and leave the rest part to the last column; default 0')
    parser.add_argument('--header', help='Headers for the Html Table')

    #mail body
    parser.add_argument('lines', nargs='*', help="zero or more lines of email body, split to columns by FS; if not received via command lines, `<` or `<<<` can be used.")

    args=parser.parse_args()
    if not args.lines:
        while True:
            try:
                args.lines.append(raw_input())
            except EOFError, e:
                break
    return args


def msg(args):
    m=Message(To=re.split(r'[\s;,]+', args.to),
              From=args.frm,
              Subject=args.subject,
              charset='utf-8'
              )
    m.Html=str(HTMLTable(args))

    sender=Mailer(host=args.host,
                  port=args.port,
                  usr=args.username,
                  pwd=args.password)
    if args.port==587:
        sender.use_tls=True
    sender.send(m)

def main():
    args=getArgs()
    msg(args)


if __name__=='__main__':
    main()
