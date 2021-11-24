buyers = new FeedObject('/json_buyers/');

buyers.me = 'buyers';

buyers.all = function(domid, items, options)
{
    options['isotope'] = true;
    var output = [], item, lastcontact, lock, js = "javascript:buyers.updatesilent(null,{'togglelock' : {} });buyers.display();";
    for (var i=0; i<items.length; i++)
    {
        item = items[i];
        if (item.hot) lock = staticimage('locked.png'); else lock = staticimage('unlocked.png');;
        lastcontact = item.last_contact?moment(item.last_contact).fromNow():'Jamais contacté';
        card = {
                    'title' : '<a href="/client/#'+item.client_id+'">'+(item.budget?'&euro;'+numberWithCommas(item.budget)+' - ':'')+item.what+'</a>'+'<a class="pull-right" href="'+js.replace("{}", item.client_id)+'">'+lock+'<a>',
                    'body' : this.readmore(item.description, '/client/#'+item.client_id)+(item.tags && item.tags.length > 0?'<hr/>'+this.taglist(item.tags):''),
                   'footer' : lastcontact+' '+item.who,
                };

        output.push({ search: item.search, infinitescroll : item.infinitescroll, html: card_display(card) });
    }
    this.list(domid, output, options);
}

buyers.single = function(domid, items, options)
{
    options['wrapper'] = 'panel';
    var output = [];
    for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ search: item.search, infinitescroll : item.infinitescroll, html: panelTop('Recherche '+item.what+(item.budget?' - &euro;'+numberWithCommas(item.budget):''), { 'Modifier' : 'javascript:buyers.modal(\'#modal\', { title : \'Modifier recherche\', hidden: { id: '+item.id+' } });', 'Supprimer' : 'javascript:buyers.modal_delete(\'#modal\',  '+item.id+');' })+panelBody('<a href="javascript:buyers.modal(\'#modal\', { title : \'Modifier recherche\', hidden: { id: '+item.id+' } });">'+divRow(divCol(safe_html(item.description)))+'<hr/>'+divRow(divCol(this.taglist(item.tags, false, 'btn-default btn-sm'),10)+divCol(moment(item.date_created).format("MMM Do YYYY"),2))+'</a>') });
    }
    this.list(domid, output, options);
}

buyers.form = function()
{
    return [
                [
                    [{ type: 'select', field: 'what', title: '', options: { 'appartement': 'Appartement', 'villa': 'Villa', 'commerce': 'Commerce', 'terrain': 'Terrain', 'garage': 'Garage' }, 'default': 'appartement' } ],
                    [{ type: 'input', field: 'budget', title: 'Budget' }],
                ],
                [
                    
                    [{ type: 'input', field: 'tags', title: 'Tags' }],
                ],
                { type: 'textarea', field: 'description', title: 'Notes' },
            ];
}

buyers.trash = ["Achet&eacute; avec moi", "Achet&eacute; avec un autre agence", "Achet&eacute; par un particulier", "N'achete plus dans cette region", "N'achete plus de tout", "Pas serieux"];
