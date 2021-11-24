agentfactures = new FeedObject('/json_agent_factures/');

agentfactures.me = 'agentfactures';

agentfactures.all = function(domid, items, options)
{
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        html = concat_cells({   'cell_open' : "<td "+(item.paid!='true'?' style="background-color:red;"':'')+"><a href=\"javascript:agentfactures.modal('#modal', { title : 'Modifier facture', hidden: { id: "+item.id+" } });\">",
                                'cell_close': '</a></td>',
                                'cells' : [item.date, '#'+item.invoice_number, item.agent, item.sale, (item.commission?showPrice(item.commission):item.commission_percent+'%')]
                            });
        output.push({ infinitescroll : item.infinitescroll, html: html });
    }
    this.list(domid, output, options);
}

agentfactures.form = function()
{
    return [
                { type: 'input', field: 'invoice_number', title: 'Numero facture' },
                [
                    [{ type: 'select2', field: 'agent_id', title: 'Agent', options: myagency.options('fullname') }],
                    [{ type: 'select2', field: 'sale_id', title: 'Vente', options: notairefactures.options('description') }],
                ],
                [
                    [{ type: 'select', field: 'commission_percent', title: 'Partage ', options : { '25' : '25%',  '50' : '50%' }, width : 3 }],
                ],
                [
                    [{ type: 'input', field: 'commission', title: 'ou montant fixe' }],
                    [{ type: 'boolean', field: 'vat', title: 'TVA inclus', 'default': 'true' }],
                    [{ type: 'boolean', field: 'paid', title: 'Paid', 'default': 'false' }],
                ],
                 { type: 'date', field: 'date', title: 'Date du facture', required: true }
            ];
}
