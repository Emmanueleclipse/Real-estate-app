suppliers = new FeedObject('/json_suppliers/');

suppliers.me = 'suppliers';

suppliers.all = function(domid, items, options)
{
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ 'search': item.name.toLowerCase()+' '+item.tags.toLowerCase(), infinitescroll : item.infinitescroll, html: "<td><a href=\"javascript:suppliers.modal('#modal', { title : 'Modifier fournisseur', hidden: { id: "+item.id+" } });\">"+item.name+'</a></td><td>'+(item.tags?item.tags:'')+'</td><td>'+(item.description?item.description:'')+'</td>' });
    }
    this.list(domid, output, options);
}

suppliers.form = function()
{
    return [
                { type: 'input', field: 'name', title: 'Fournisseur', required: true },
                { type: 'textarea', field: 'description', title: 'Descriptif' },
                [
                    [{ type: 'input', field: 'siret', title: 'SIRET' }],
                    [{ type: 'input', field: 'vat_number', title: 'Numero TVA' }],
                    [{ type: 'input', field: 'category', title: 'Categorie' }],
                ],
                { type: 'input', field: 'tags', title: 'Tags' },
             ];
}

suppliers_facture = new FeedObject('/json_suppliers_facture/');

suppliers_facture.me = 'suppliers_facture';

suppliers_facture.all = function(domid, items, options)
{
    var item, html;
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    for (var i=0; i<items.length; i++)
    {
        item = items[i];
        html = concat_cells({ 'cell_open' : "<td "+(item.paid!='true'?' style="background-color:red;"':'')+"><a href=\"javascript:suppliers_facture.modal('#modal', { title : 'Modifier facture', hidden: { id: "+item.id+" } });\">", 'cell_close': '</a></td>', 'cells' : [item.date, item.supplier, '&euro;'+item.amount, item.description] });
        output.push({ 'search': item.supplier.toLowerCase()+(item.description?' '+item.description.toLowerCase():''), infinitescroll : item.infinitescroll, html: html });
    }
    this.list(domid, output, options);
}

suppliers_facture.form = function()
{
    return [
                { type: 'select2', field: 'supplier', title: 'Fournisseur', options: suppliers.options('name'), required: true },
                { type: 'input', field: 'invoice_number', title: 'Numero facture', required: true },
                [
                    [{ type: 'input', field: 'amount', title: 'Montant', required: true }],
                    [{ type: 'boolean', field: 'vat', title: 'TVA inclus', 'default': 'true' }],
                    [{ type: 'boolean', field: 'paid', title: 'Paid', 'default': 'false' }],
                ],
                { type: 'textarea', field: 'description', title: 'Descriptif' },
                { type: 'date', field: 'date', title: 'Date du facture', required: true }
            ];
}
