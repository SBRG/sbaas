#!/usr/bin/env python
# -*- coding: utf-8 -*-
# molmass_cgi.py

# Copyright (c) 2005-2014, Christoph Gohlke
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the names of any
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Molecular Mass Calculator - A common gateway interface for molmass.py.

Run ``python molmass_cgi.py`` to execute the script in a local web server.

:Author: `Christoph Gohlke <http://www.lfd.uci.edu/~gohlke/>`_

:Version: 2013.03.18

Requirements
------------
* `CPython 2.7 or 3.3 <http://www.python.org>`_
* `Molmass.py 2013.03.18 <http://www.lfd.uci.edu/~gohlke/>`_
* `Elements.py 2013.03.18 <http://www.lfd.uci.edu/~gohlke/>`_

"""

from __future__ import division, print_function

import os
import re
import sys
import cgi

if sys.version_info[0] == 2:
    from urlparse import urlunsplit
else:
    from urllib.parse import urlunsplit


def response(form, template=None, result=None):
    """Return HTML document from submitted form data."""

    if template is None:
        template = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="generator" content="molmass_cgi.py" />
        <meta name="robots" content="noarchive, nofollow" />
        <title>Molecular Mass Calculator</title>
        </head>
        <body>
        <h1><a href="%(url)s" style="text-decoration:none;color:#000000">
        Molecular Mass Calculator</a></h1>
        <form id="form" method="get" action="">
        <div>
        <label><strong>Formula: </strong>
        <input name="q" type="text" id="q" size="50" value="%(formula)s" />
        </label>
        <label>
        <input type="submit" id="a" value="Submit" />
        </label>
        <label>
        <input type="reset" value="Reset" onclick="window.location='%(url)s'"/>
        </label>
        </div>
        </form>
        <div class="content">
        %(result)s
        </div>
        </body>
        </html>
        """

    if result is None:
        result = """
        <p>This form calculates the molecular mass (average, monoisotopic,
        and nominal), the elemental composition, and the mass distribution
        spectrum of a molecule given by its chemical formula, relative element
        weights, or sequence.</p>
        <p>Calculations are based on the
        <a href="?q=isotopes">isotopic composition of the elements</a>.
        Mass deficiency due to chemical bonding is not taken into account.
        </p>
        <h3>Examples</h3>
        <ul>
        <li>Simple chemical formulas:
        <a href="?q=H2O">H2O</a> or
        <a href="?q=CH3COOH">CH3COOH</a>
        </li>
        <li>Specific isotopes:
        <a href="?q=D2O">D2O</a> or
        <a href="?q=[30Si]3O2">[30Si]3O2</a>
        </li>
        <li><a href="?q=groups">Abbreviations</a> of chemical groups:
        <a href="?q=EtOH">EtOH</a> or
        <a href="?q=PhOH">PhOH</a>
        </li>
        <li>Simple arithmetic:
        <a href="?q=(COOH)2">(COOH)2</a> or
        <a href="?q=CuSO4.5H2O">CuSO4.5H2O</a>
        </li>
        <li>Relative element weights:
        <a href="?q=O: 0.26, 30Si: 0.74">O: 0.26, 30Si: 0.74</a>
        </li>
        <li>Nucleotide sequences:
        <a href="?q=CGCGAATTCGCG">CGCGAATTCGCG</a> or
        <a href="?q=dsrna(CCUU)">dsrna(CCUU)</a>
        </li>
        <li>Peptide sequences:
        <a href="?q=MDRGEQGLLK">MDRGEQGLLK</a> or
        <a href="?q=peptide(CPK)">peptide(CPK)</a>
        </li>
        </ul>
        <p>Formulas are case sensitive and &#8217;+&#8217; denotes
        the arithmetic operator, not an ion charge.</p>
        <h3>Disclaimer</h3>
        <p>Because this service is provided free of charge, there is no
        warranty for the service, to the extent permitted by applicable law.
        The service is provided &quot;as is&quot; without warranty of any kind,
        either expressed or implied, including, but not limited to, the implied
        warranties of merchantability and fitness for a particular purpose.
        The entire risk as to the quality and performance is with you.</p>
        <h3>Credits</h3>
        <p>Developed by
        <a href="http://www.lfd.uci.edu/~gohlke/">Christoph Gohlke</a>,
        <a href="http://www.lfd.uci.edu">Laboratory for Fluorescence
        Dynamics</a>.
        Source code is available under BSD license.
        """

    formula = form.getfirst('q')
    if not formula:
        formula = ''
    if formula == 'groups':
        formula = ''
        result = groups()
    elif formula == 'isotopes':
        formula = ''
        result = isotopes()
    elif formula:
        result = analyze(formula[:100])
    result = template % {
        'url': script_url(),
        'result': result,
        'formula': cgi.escape(formula, True)}
    return result.replace('    ', '')


def analyze(formula, maxatoms=250):
    """Return analysis of formula as HTML string."""

    import molmass

    def html(formula):
        """Return formula as HTML string."""
        formula = re.sub(
            "\[(\d+)([A-Za-z]{1,2})\]", "<sup>\\1</sup>\\2", formula)
        formula = re.sub(
            "([A-Za-z]{1,2})(\d+)", "\\1<sub>\\2</sub>", formula)
        return formula

    result = []
    try:
        f = molmass.Formula(formula)
        result.append(
            '<p><strong>Hill notation</strong>: %s</p>' % html(f.formula))
        if f.formula != f.empirical:
            result.append(
                '<p><strong>Empirical formula</strong>: %s</p>' % html(
                    f.empirical))

        prec = molmass.precision_digits(f.mass, 8)
        if f.mass != f.isotope.mass:
            result.append(
                '<p><strong>Average mass</strong>: %.*f</p>' % (prec, f.mass))
        result.extend((
            '<p><strong>Monoisotopic mass</strong>: %.*f</p>' % (
                prec, f.isotope.mass),
            '<p><strong>Nominal mass</strong>: %i</p>' % f.isotope.massnumber))

        c = f.composition()
        if len(c) > 1:
            result.extend((
                '<h3>Elemental Composition</h3>'
                '<table border="0" cellpadding="2">',
                '<tr>',
                '<th scope="col" align="left">Element</th>',
                '<th scope="col" align="right">Number</th>',
                '<th scope="col" align="right">Relative mass</th>',
                '<th scope="col" align="right">Fraction %</th>',
                '</tr>'))

            for symbol, count, mass, fraction in c:
                symbol = re.sub("^(\d+)(.+)", "<sup>\\1</sup>\\2", symbol)
                result.extend((
                    '<tr><td>%s</td>' % symbol,
                    '<td align="center">%i</td>' % count,
                    '<td align="right">%.*f</td>' % (prec, mass),
                    '<td align="right">%.4f</td></tr>' % (fraction * 100)))

            count, mass, fraction = c.total
            result.extend((
                '<tr><td><em>Total</em></td>',
                '<td align="center"><em>%i</em></td>' % count,
                '<td align="right"><em>%.*f</em></td>' % (prec, mass),
                '<td align="right"><em>%.4f</em></td></tr>' % (fraction * 100),
                '</table>'))

        if f.atoms < maxatoms:
            s = f.spectrum()
            if len(s) > 1:
                norm = 100.0 / s.peak[1]
                result.extend((
                    '<h3>Mass Distribution</h3>',
                    '<p><strong>Most abundant mass</strong>: ',
                    '%.*f (%.3f%%)</p>' % (prec, s.peak[0], s.peak[1] * 100),
                    '<p><strong>Mean mass</strong>: %.*f</p>' % (prec, s.mean),
                    '<table border="0" cellpadding="2">',
                    '<tr>',
                    '<th scope="col" align="left">Relative mass</th>',
                    '<th scope="col" align="right">Fraction %</th>',
                    '<th scope="col" align="right">Intensity</th>',
                    '</tr>'))
                for mass, fraction in s.values():
                    result.extend((
                        '<tr><td>%.*f</td>' % (prec, mass),
                        '<td align="right">%.6f</td>' % (fraction * 100.0),
                        '<td align="right">%.6f</td></tr>' % (fraction*norm)))
                result.append('</table>')

    except Exception as e:
        e = str(e).splitlines()
        text = e[0][0].upper() + e[0][1:]
        details = '\n'.join(e[1:])
        result.append('<h2>Error</h2><p>%s</p><pre>%s</pre>' % (text, details))

    return "\n".join(result)


def isotopes():
    """Return table of isotope masses and abundances as HTML string."""

    import molmass

    template = """<h3>Isotopic Composition of the Elements</h3>
    <table border="0" cellpadding="2">
    <tr>
    <th align="left" scope="col">Element/Isotope</th>
    <th align="right" scope="col">Relative mass</th>
    <th align="right" scope="col">Abundance</th>
    </tr>
    %s
    </table>"""

    result = []
    for ele in molmass.ELEMENTS:
        result.extend((
            '<tr><td><em>%s</em></td>' % ele.name,
            '<td align="right">%12.8f</td></tr>' % ele.mass))
        for massnumber in sorted(ele.isotopes):
            iso = ele.isotopes[massnumber]
            result.extend((
                '<tr><td align="right"><sup>%i</sup>%s</td>' % (
                    massnumber, ele.symbol),
                '<td align="right">%.8f</td>' % iso.mass,
                '<td align="right">%.8f</td></tr>' % (iso.abundance * 100.0)))
    result = "\n".join(result)
    return template % result


def groups():
    """Return table of chemical groups as HTML string."""

    import molmass

    template = """<h3>%s</h3>
    <table border="0" cellpadding="2">
    <tr>
    <th align="left" scope="col">Name</th>
    <th align="left" scope="col">Formula</th>
    </tr>
    %s
    </table>"""

    result = []
    for groups, title in ((molmass.GROUPS, "Chemical Groups"),
                          (molmass.AMINOACIDS, "Amino Acids"),
                          (molmass.DEOXYNUCLEOTIDES, "Deoxynucleotides"),
                          (molmass.NUCLEOTIDES, "Nucleotides")):
        tmp = []
        for key in sorted(groups):
            value = groups[key]
            if isinstance(value, basestring if sys.version[0] == '2' else str):
                tmp.append("<tr><td>%s</td><td>%s</td></tr>" % (key, value))
        result.append(template % (title, "\n".join(tmp)))
    return "\n".join(result)


def script_path():
    """Return path to CGI script."""
    result = os.getenv('PATH_TRANSLATED')
    if '.py' in result:
        result = os.path.dirname(result)
    return result


def script_url(env=os.getenv):
    """Return URL of CGI script, without script name if that is index.py."""
    netloc = env('SERVER_NAME')
    port = env('SERVER_PORT')
    path = env('SCRIPT_NAME')
    if not '.' in netloc:
        netloc = _LOCALHOST
    if port and port != '80':
        netloc += ':' + port
    if path is None:
        path = env('PATH_INFO')
    if path is None:
        path = ''
    elif path.endswith('index.py'):
        path = path.rsplit('/', 1)[0] + '/'
    scheme = 'https' if (port and int(port) == 443) else 'http'
    return urlunsplit([scheme, netloc, path, '', ''])


def is_cgi(self):
    """Monkey patch for CGIHTTPRequestHandler.is_cgi()."""
    if _NAME in self.path:
        self.cgi_info = '', self.path[1:]
        return True
    return False


_LOCALHOST = "0.0.0.0"
_LOCALPORT = 9000
_NAME = os.path.split(__file__)[-1]

if __name__ == "__main__":
    if os.getenv('SERVER_NAME'):
        print("Content-type: text/html\n\n")
        print(response(cgi.FieldStorage()))
    else:
        import webbrowser
        import cgitb
        cgitb.enable()
        if sys.version_info[0] == 2:
            from BaseHTTPServer import HTTPServer
            from CGIHTTPServer import CGIHTTPRequestHandler
        else:
            from http.server import HTTPServer, CGIHTTPRequestHandler
        CGIHTTPRequestHandler.is_cgi = is_cgi
        _url = "http://localhost:%i/%s" % (_LOCALPORT, _NAME)
        print("Serving CGI script at", _url)
        webbrowser.open(_url)
        HTTPServer((_LOCALHOST, _LOCALPORT),
                   CGIHTTPRequestHandler).serve_forever()