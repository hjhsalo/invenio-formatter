# -*- coding: utf-8 -*-
## $Id$

## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005 CERN.
##
## The CDSware is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## The CDSware is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDSware; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

def format(bfo, limit, separator=' ; ',extension='[...]', print_links="yes", interactive="no"):
    """
    Prints the list of authors of a record.
    
    @param limit the maximum number of authors to display
    @param separator the separator between authors.
    @param extension a text printed if more authors than 'limit' exist
    @param print_links if yes, prints the authors as HTML link to their publications
    @param interactive if yes, enable user to show/hide authors when there are too many (html + javascript)
    """
    from urllib import quote
    from invenio.config import weburl
    from invenio.messages import gettext_set_language
    
    _ = gettext_set_language(bfo.lang)    # load the right message language
    
    authors = []
    authors_1 = bfo.fields('100.a')
    authors_2 = bfo.fields('700.a')
    authors_3 = bfo.fields('270.p')

    authors.extend(authors_1)
    authors.extend(authors_2)
    authors.extend(authors_3)

    if print_links.lower() == "yes":
        authors = map(lambda x: '<a href="'+weburl+'/search.py?f=author&p='+ quote(x) +'">'+x+'</a>', authors)

    if limit.isdigit() and len(authors) > int(limit) and interactive != "yes":
        return separator.join(authors[:int(limit)]) + extension

    elif limit.isdigit() and len(authors) > int(limit) and interactive == "yes":
        out = '''
        <SCRIPT>
        function toggle_authors_visibility(){
            var more = document.getElementById('more');
            var link = document.getElementById('link');
            var extension = document.getElementById('extension');
            if (more.style.display=='none'){
                more.style.display = '';
                extension.style.display = 'none';
                link.innerHTML = "%(show_less)s"
            } else {
                more.style.display = 'none';
                extension.style.display = '';
                link.innerHTML = "%(show_more)s"
            } 
        }
        </SCRIPT>
        '''%{'show_less':_("Show Less"), 'show_more':_("Show All")}
        out += '<a name="show_hide" />'
        out += separator.join(authors[:int(limit)])
        out += '<span id="more" style="display:none;">'+separator.join(authors[int(limit):])+'</span>'
        out += ' <span id="extension">%s</span>'%extension
        out += ' <small><i><a id="link" href="#show_hide" onclick="toggle_authors_visibility()">%s</a></i></small>'%_("Show All")

        return out
    elif len(authors) > 0:
        return separator.join(authors)
