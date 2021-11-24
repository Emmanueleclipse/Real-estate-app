

notairefactures.summary = function(domid, items, options)
{
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    var items = notairefactures.data;
    var totals = {}, yeartotal, year, month, item, firstyear = false, lastyear = false;
    for (var i=0; i<items.length; i++)
    {
        item = items[i];
        month = item.date.substring(0,7);
        year = parseInt(item.date.substring(0,4));
        if (month in totals) totals[month]['amount'] = totals[month]['amount'] + parseInt(item.commission); else totals[month] = { 'amount' : parseInt(item.commission), 'month' : month, 'year' : false };
        if (!firstyear || firstyear > year) firstyear = year;
        if (!lastyear || lastyear < year) lastyear = year;
    }
    for (var yi = lastyear; yi > firstyear-1; yi--)
    {
        html = concat_cells({   'cell_open' : "<td><b>", 'cell_close': '</b></td>',
                                'cells' : [yi.toString(), 'Commission',  'TVA', 'Net']
                            });
        output.push({ infinitescroll : item.infinitescroll, html: html });
        yeartotal = 0;
        for (var mi = 1; mi < 13; mi++)
        {
            month = yi.toString()+'-'+mi.toString().padStart(2, '0');
            if (month in totals) { item = totals[month]; yeartotal = yeartotal + item.amount; }
            else item = { 'amount' : false, 'month' : month };
            html = concat_cells({   'cell_open' : "<td>",
                                'cell_close': '</td>',
                                'cells' : [monthname(mi), (item.amount?showPrice(item.amount):'-'),(item.amount?showPrice(item.amount-item.amount/1.2):'-'),(item.amount?showPrice(item.amount/1.2):'-')]
                            });
            output.push({ infinitescroll : item.infinitescroll, html: html });
        }
        html = concat_cells({   'cell_open' : "<td><i>", 'cell_close': '</i></td>',
                                'cells' : [ 'Total', (yeartotal?showPrice(yeartotal):'-'),(yeartotal?showPrice(yeartotal-yeartotal/1.2):'-'),(yeartotal?showPrice(yeartotal/1.2):'-')]
                            });
        output.push({ infinitescroll : item.infinitescroll, html: html });
     }
    this.list(domid, output, options);
}

suppliers_facture.summary = function(domid, items, options)
{
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    var items = suppliers_facture.data;
    var totals = {}, yeartotal, yearvat, yearnet, year, month, vat, item, firstyear = false, lastyear = false;
    for (var i=0; i<items.length; i++)
    {
        item = items[i];
        month = item.date.substring(0,7);
        year = parseInt(item.date.substring(0,4));
        if (month in totals) totals[month]['amount'] = totals[month]['amount'] + parseInt(item.amount); else totals[month] = { 'amount' : parseInt(item.amount), 'month' : month, 'vat' : item.vat };
        if (!firstyear || firstyear > year) firstyear = year;
        if (!lastyear || lastyear < year) lastyear = year;
    }
    for (var yi = lastyear; yi > firstyear-1; yi--)
    {
        html = concat_cells({   'cell_open' : "<td><b>", 'cell_close': '</b></td>',
                                'cells' : [yi.toString(), 'Commission',  'TVA', 'Net']
                            });
        output.push({ infinitescroll : item.infinitescroll, html: html });
        yeartotal = 0; yearvat =0; yearnet = 0;
        for (var mi = 1; mi < 13; mi++)
        {
            month = yi.toString()+'-'+mi.toString().padStart(2, '0');
            if (month in totals) { item = totals[month]; yeartotal = yeartotal + item.amount; yearvat = yearvat + (item.vat?(item.amount-item.amount/1.2):0); yearnet = yearnet + (item.vat?item.amount/1.2:item.amount); }
            else item = { 'amount' : false, 'month' : month };
            html = concat_cells({   'cell_open' : "<td>",
                                'cell_close': '</td>',
                                'cells' : [monthname(mi), (item.amount?showPrice(item.amount):'-'),(item.amount?showPrice(item.amount-item.amount/1.2):'-'),(item.amount?showPrice(item.amount/1.2):'-')]
                            });
            output.push({ infinitescroll : item.infinitescroll, html: html });
        }
        html = concat_cells({   'cell_open' : "<td><i>", 'cell_close': '</i></td>',
                                'cells' : [ 'Total', showPrice(yeartotal),showPrice(yearvat),showPrice(yearnet)]
                            });
        output.push({ infinitescroll : item.infinitescroll, html: html });
     }
    this.list(domid, output, options);
}
