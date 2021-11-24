addclientlead = new FeedObject('/json_addclientlead/');

addclientlead.me = 'addclientlead';

addclientlead.menu = function(domid, items, options)
{
    options['wrapper'] = 'span';
    output = [];

    if (items.length>0) for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        if (item.failed) output.push({ html: 'Failure: '+item.name+'<hr/>' });
        else output.push({ html: '<a class="sidemenulink" href="/client/#'+item.client_id+'"><i class="fa fa-check fa-lg">'+item.name+'</i></a><br/>' });
    }
    output.push({ html: '<a class="sidemenulink" href="javascript:addclientlead.modal(\'#modal\', {  title : \'Nouveau client\' });">Nouveau</a>' });
    this.list(domid, output, options);
}

addclientlead.form = function()
{
    return [
                { type: 'textarea', field: 'description', title: 'Description', required: true },
                [
                    [{ type: 'input', field: 'name', title: 'Nom', required: true }],
                    [{ type: 'input', field: 'price', title: 'Budget' }],
                ],
                [
                    [{ type: 'input', field: 'phone', title: 'Phone' }],
                    [{ type: 'input', field: 'email', title: 'Email' }],
                ],
                [
                    [{ type: 'select', field: 'source', title: 'Source', options: { 'Passage': 'Passage', 'Phone': 'Telephone', 'Email': 'Email', 'Recommendation': 'Relationnelle' }, }],
                    [{ type: 'select', field: 'language', title: 'Langue', options: { 'fr': 'Francais', 'en': 'Anglais', 'it': 'Italien', 'ru': 'Russe' } , 'default' : 'fr' }],
                    [{ type: 'select', field: 'buysell', title: 'Pour', options : { buy: 'Achat', sell: 'Vente'}, 'default' : 'buy'}],
                    [{ type: 'select', field: 'what', title: 'Cherche', options: { 'appartement': 'Appartement', 'villa': 'Villa', 'commerce': 'Commerce', 'terrain': 'Terrain', 'garage': 'Garage' }, 'default': 'appartement' } ],
                ],
             ];
}
