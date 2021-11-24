agents = new FeedObject('/json_agents/');

agents.me = 'agents';

agents.all = function(domid, items, options)
{
    options['isotope'] = true;
    var card;
    var output = [], item;
    for (i=0; i<items.length; i++)
    {
        item = items[i];
        contacts = { 'id' : item.id, 'telephone' : (item.mobile?[{ 'number' : item.mobile, 'type' : item.type }]:null), 'email' : (item.email?[{'email' : item.email, 'type' : item.type }]:null), 'chat' : (item.isonline?item.id:null) };
        contacts['extras'] = [{ 'icon' : 'home', 'text' : 'Agence', 'href': '/agence/#'+item.agency_id }];
        card = {
                    'title' : item.forename+' '+item.surname,
                    'titleactions' : [],
                    'body' : card_contactbar(contacts),
                    'footer' : '<a href="/agence#'+item.agency_id+'">'+item.agency+'</a>',
                };
        if (isadmin) card['titleactions'].push({ 'icon' : 'edit', 'action' : 'agents.modal(\'#modal\', { title : \'Modifier agent\', hidden: { id: '+item.id+' } })' });
        output.push({ 'class': 'card', search: item.search, infinitescroll : item.infinitescroll, html: card_display(card) });
    }
    this.list(domid, output, options);
}

agents.globalsearch = function(domid, items, options)
{
    var output = [];

    if (items.length ==0) output.push({ 'class': 'list-group-item', 'html': '0 resultat' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ 'html': '<li><a href="/agence/#'+String(item.agency_id)+'"'+(window.location.href.indexOf('/agence/')?' onclick="location.hash=\''+String(item.agency_id)+'\'; location.reload();"':'')+'>'+item.forename+' '+item.surname+'</a></li>' });
    }

    this.list(domid, output, options);

}

agents.form = function()
{
    return [
                { type: 'input', field: 'forename', title: 'Forename' },
                { type: 'input', field: 'surname', title: 'Surname' },
                { type: 'input', field: 'role', title: 'Role' },
                { type: 'input', field: 'mobile', title: 'Mobile' },
                { type: 'input', field: 'email', title: 'Email' },
                { type: 'boolean', field: 'public', title: 'Public' },
            ];
}
