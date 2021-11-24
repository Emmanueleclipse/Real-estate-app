clientleads = new FeedObject('/json_clientleads/');

clientleads.me = 'clientleads';

clientleads.all = function(domid, items, options)
{
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    for (i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ 'search': item.name.toLowerCase()+' '+item.source.toLowerCase()+' '+item.agent.toLowerCase(), infinitescroll : item.infinitescroll, html: '<td>'+moment(item.date_created).fromNow()+'</td><td><a href="/client/#'+item.client_id+'">'+item.name+'</a></td><td>'+item.source+'</td><td>&euro;'+numberWithCommas(item.price)+'</td><td>'+(item.buying?"Buying ":"Selling ")+item.what+'</td><td>'+item.agent+'</td>' });
    }
    this.list(domid, output, options);
}

clientleads.form = function()
{
    return [
                { type: 'textarea', field: 'description', title: 'Description' },
                [
                    [{ type: 'input', field: 'name', title: 'Nom' }],
                    [{ type: 'input', field: 'budget', title: 'Budget' }],
                ],
                [
                    [{ type: 'input', field: 'budget', title: 'Phone' }],
                    [{ type: 'input', field: 'budget', title: 'Email' }],
                ],
                [
                    [{ type: 'select', field: 'source', title: 'Source', options: { 'Passage': 'Passage', 'Phone': 'Telephone', 'Email': 'Email', 'Recommendation': 'Relationnelle' }, }],
                    [{ type: 'select', field: 'language', title: 'Langue', options: { 'fr': 'Francais', 'en': 'Anglais', 'it': 'Italien', 'ru': 'Russe' } , 'default' : 'fr' }],
                    [{ type: 'select', field: 'buysell', title: 'Pour', options : { buy: 'Achat', sell: 'Vente'}, 'default' : 'buy'}],
                    [{ type: 'select', field: 'what', title: 'Cherche', options: { 'appartement': 'Appartement', 'villa': 'Villa', 'commerce': 'Commerce', 'terrain': 'Terrain', 'garage': 'Garage' }, 'default': 'appartement' } ],
                ],
             ];
}
