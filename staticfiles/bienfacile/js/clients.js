clients = new FeedObject('/json_clients/');
clients.clientstatus = function(domid, items, options)
{
    if (items.length == 0 || !items[0]) window.location.replace("/clients/");
    client = items[0];
    if (client.trash) $(domid).html('<em>'+client.name+' - '+client.trash+'</em>');
    else
    {
        if (client.next_contact) var lastcontact = 'prochaine contact <i class="fa fa-calendar"></i> '+moment(client.next_contact).fromNow(); else if (client.last_contact) var lastcontact = 'dernier contact <i class="fa fa-clock-o"></i> '+moment(client.last_contact).fromNow(); else var lastcontact = 'jamais contacté';
        $(domid).html(client.name+' - '+lastcontact);
    }
}
clients.globalsearch = function(domid, items, options)
{
    var output = [];

    if (items.length ==0) output.push({ 'class': 'list-group-item', 'html': '0 resultat' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ 'html': '<li><a href="/client/#'+String(item.id)+'"'+(window.location.href.indexOf('/clients/')?' onclick="location.hash=\''+String(item.id)+'\'; location.reload();"':'')+'>'+item.name+'</a></li>' });
    }

    this.list(domid, output, options);

}
clients.me = 'clients';
clients.trash = ["Utilise une autre agence", "N'achete plus dans cette region", "N'achete plus de tout", "Ne reponds plus", "Acheteur pas serieux", "Problèmes financiers", "Problèmes de santé",];
