apporteurfactures = new FeedObject('/json_apporteur_factures/');

apporteurfactures.me = 'apporteurfactures';

apporteurfactures.all = function(domid, items, options)
{
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        html = concat_cells({   'cell_open' : "<td "+(item.paid!='true'?' style="background-color:red;"':'')+"><a href=\"javascript:apporteurfactures.modal('#modal', { title : 'Modifier facture', hidden: { id: "+item.id+" } });\">",
                                'cell_close': '</a></td>',
                                'cells' : [item.date, '#'+item.invoice_number, item.name, showPrice(item.commission), item.sale, item.agent]
                            });
        output.push({ infinitescroll : item.infinitescroll, html: html });
    }
    this.list(domid, output, options);
}

apporteurfactures.form = function()
{
    return [
                { type: 'input', field: 'invoice_number', title: 'Numero facture' },
                [
                    [{ type: 'select2', field: 'agent_id', title: 'Agent', required: true, options: myagency.options('fullname') }],
                    [{ type: 'select2', field: 'sale_id', title: 'Vente', required: true, options: notairefactures.options('description') }],
                ],
                [
                    [{ type: 'input', field: 'name', title: 'Nom', required: true }],
                    [{ type: 'input', field: 'siret', title: 'SIRET' }],
                ],
                { type: 'input', field: 'address', title: 'Adresse', required: true },
                [
                    [{ type: 'input', field: 'iban', title: 'IBAN', required: true }],
                    [{ type: 'input', field: 'bic', title: 'BIC' }],
                ],
                [
                    [{ type: 'input', field: 'commission', title: 'Commission', required: true }],
                    [{ type: 'boolean', field: 'vat', title: 'TVA inclus', 'default': 'true' }],
                    [{ type: 'boolean', field: 'paid', title: 'Paid', 'default': 'false' }],
                ],
                 { type: 'date', field: 'date', title: 'Date du facture', required: true }
            ];
}
