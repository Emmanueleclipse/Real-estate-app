
agences = new FeedObject('/json_agences/');

agences.me = 'agences';

agences.short_address = function(address) { return address.replace('Boulevard', 'Bvd').replace('Avenue', 'Av.').replace(', ', ' '); }

agences.card_agence = function(item) {
        contacts = { 'id' : item.id, 'telephone' : (item.telephone?[{ 'number' : item.telephone, 'type' : item.type }]:null), 'email' : (item.email?[{ 'email' : item.email, 'type' : item.type }]:null) }
        if (item.web) contacts['extras'] =  [ { 'icon' : 'web', 'text' : 'Web', 'href' : item.web }];
        card = {
                    'title' : '<a href="/agence/#'+item.id+'">'+item.name+'</a>'+(item.branch?'<br/><small>('+item.branch+')</small>':''),
                    'body' : card_contactbar(contacts),
                    'footer' : this.short_address(item.address)+' '+item.postcode+' '+item.city
                };
        return card_display(card);
}

agences.all = function(domid, items, options)
{
    options['isotope'] = true;
    var output = [], item;
    for (i=0; i<items.length; i++)
    {
        item = items[i];
        output.push({ 'class' : 'card', search: item.search, infinitescroll : item.infinitescroll, html: this.card_agence(item) });
    }
    this.list(domid, output, options);
}

agences.single = function(domid, items, options)
{
    options['isotope'] = false;
    var agency = this.getdata(options['id']); var attach = [];
    if (!agency) { alert("Not found agency id "+options['id']); return; }
    if (!agents) { alert("Not found 'agents' dependency"); return; }
    items = this.match('name', agency.name);
    var output = [], item;
    for (var i=0; i<items.length; i++)
    {
        item = items[i];
        output.push({ 'class' : 'cardfull', search: item.search, infinitescroll : item.infinitescroll, html: this.card_agence(item), footer: '<div id="agents_'+item.id+'">Loading...</div>' });
        attach.push("agents.attach('#agents_"+item.id+"', 'all', { filter : { agency_id: "+item.id+" }, childwrapper_class : 'agentsItem'});");
    }
    options['footer'] = "<script>\n"+attach.join("\n")+"</script>";
    this.list(domid, output, options);
}

agences.globalsearch = function(domid, items, options)
{
    var output = [];

    if (items.length ==0) output.push({ 'class': 'list-group-item', 'html': '0 resultat' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ 'html': '<li><a href="/agence/#'+String(item.id)+'"'+(window.location.href.indexOf('/agence/')?' onclick="location.hash=\''+String(item.id)+'\'; location.reload();"':'')+'>'+item.name+(item.branch?' ('+item.branch+')':'')+'</a></li>' });
    }

    this.list(domid, output, options);
}

agences.form = function()
{
    return [
                [
                    [{ type : 'select', field : 'what', title : '', options: { 'appartement': 'Appartement', 'villa': 'Villa', 'commerce': 'Commerce', 'terrain': 'Terrain', 'garage': 'Garage' }, 'default' : 'appartement' } ],
                    [{ type: 'input', field: 'budget', title: 'Budget' }],
                ],
                [
                    
                    [{ type: 'input', field: 'tags', title: 'Tags' }],
                ],
                { type: 'textarea', field: 'description', title: 'Notes' },
            ];
}
