sellers = new FeedObject('/json_sellers/');

sellers.me = 'sellers';

sellers.all = function(domid, items, options)
{
    options['isotope'] = true;
    var output = [], item, lastcontact, price, lock, js = "javascript:sellers.updatesilent(null,{'togglelock' : {} });sellers.display();";;
    for (var i=0; i<items.length; i++)
    {
        item = items[i];
        lastcontact = item.last_contact?moment(item.last_contact).fromNow():'Jamais contacté';
        price = showPrice(item.price);
        if (item.hot) lock = staticimage('locked.png'); else lock = staticimage('unlocked.png');;
        card = {
                    'title' : '<a href="/client/#'+item.client_id+'">'+(price?price+' - ':'')+item.what+'</a>'+'<a class="pull-right" href="'+js.replace("{}", item.client_id)+'">'+lock+'<a>',
                    'body' : this.readmore(item.description, '/client/#'+item.client_id)+(item.tags && item.tags.length > 0?'<hr/>'+this.taglist(item.tags):''),
                   'footer' : lastcontact+' '+item.who,
                };

        output.push({ search: item.search, infinitescroll : item.infinitescroll, html: card_display(card) });
    }
    this.list(domid, output, options);
}

sellers.single = function(domid, items, options)
{
    options['wrapper'] = 'panel';
    var output = [];
    for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ search: item.search, infinitescroll : item.infinitescroll, html: panelTop('Vente '+item.what+(item.price?' - &euro;'+numberWithCommas(item.price):'')+(item.address?' - '+item.address:''), { 'Modifier' : 'javascript:sellers.modal(\'#modal\', { title : \'Modifier vente\', hidden: { id: '+item.id+' } });', 'Supprimer' : 'javascript:sellers.modal_delete(\'#modal\', '+item.id+');' })+panelBody(divRow(divCol(item.description))+'<hr/>'+divRow(divCol(this.taglist(item.tags, false, 'btn-default btn-sm'),10)+divCol(moment(item.date_created).format("MMM Do YYYY"),2))) });
    }
    this.list(domid, output, options);
}

sellers.form = function()
{
    return [
                [
                    [{ 'type': 'select', field: 'what', title: '', 'options': { 'appartement': 'Appartement', 'villa': 'Villa', 'commerce': 'Commerce', 'terrain': 'Terrain', 'garage': 'Garage' }, 'default': 'appartement' } ],
                    [{ 'type': 'input', field: 'price', title: 'Budget' }],
                ],
                [
                    
                    [{ 'type': 'input', field: 'address', title: 'Adresse' }],
                    [{ 'type': 'input', field: 'tags', title: 'Tags' }],
                ],
                { 'type': 'textarea', field: 'description', title: 'Notes' },
            ];
}

sellers.trash = ["Mandat sign&eacute;", "Vendu avec moi", "Vendu par un autre agence", "Vendu avec un particulier", "Ne vendre pas pour maintenant", "Ne vendre plus de tout", "Pas serieux"];
