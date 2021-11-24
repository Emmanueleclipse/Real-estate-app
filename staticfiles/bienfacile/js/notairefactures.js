notairefactures = new FeedObject('/json_notaire_factures/');

notairefactures.me = 'notairefactures';

notairefactures.all = function(domid, items, options)
{
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        html = concat_cells({ 'cell_open' : "<td "+(item.paid!='true'?' style="background-color:red;"':'')+"><a href=\"javascript:notairefactures.modal('#modal', { title : 'Modifier facture', hidden: { id: "+item.id+" } });\">", 'cell_close': '</a></td>', 'cells' : [item.date, '#'+item.invoice_number, item.agent, item.client_name, item.property_address,showPrice(item.commission), item.notaire] });
        output.push({ 'search' : item.client_name.toLowerCase()+' '+item.property_address.toLowerCase(), infinitescroll : item.infinitescroll, html: html });
    }
    this.list(domid, output, options);
}

notairefactures.form = function()
{
    return [
                [
                    [{ type: 'input', field: 'commission', title: 'Commission', 'required' : true }],
                    [{ type: 'boolean', field: 'paid', title: 'Paid' , 'default' : false }],
                    [{ type: 'boolean', field: 'updatebank', title: 'Mis a jour banque', 'default' : true }],
                ],
                [
                    [{ type: 'input', field: 'invoice_number', title: 'Numero facture' }],
                    [{ type: 'input', field: 'notaire', title: 'Notaire' }],
                ],
                [
                    [{ type: 'input', field: 'client_name', title: 'Nom client', 'required' : true }],
                    [{ type: 'input', field: 'client_address', title: 'Adresse client' }],
                ],
                [
                    [{ type: 'input', field: 'property_address', title: 'Adresse du bien', 'required' : true }],
                    [{ type: 'input', field: 'other_agency', title: 'Autre agence' }],
                ],
                [
                    [{ type: 'date', field: 'date', title: 'Date', 'required' : true }],
                    [{ type: 'select2', field: 'agent_id', title: 'Agent', options: myagency.options('fullname') }],
                ]
            ];
}
