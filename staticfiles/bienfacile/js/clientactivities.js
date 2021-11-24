
clientactivities = new FeedObject('/json_recent_activities/');

clientactivities.mapping = { 'note': 'paperclip', 'email' : 'mail-reply', 'telephone' : 'phone', 'rendezvous' : 'car', 'passage' : 'building', 'web' : 'globe' }

clientactivities.all = function(domid, items, options)
{
    options['header'] = '<div class="panel panel-default">';
    options['wrapper'] = 'ul';
    output = [];
    if (items.length ==0) output.push({ 'class': 'list-group-item', html: 'Aucun activities' });
    else for (i=0; i<items.length; i++)
    {
        var item = items[i];
            output.push({ 'class': 'list-group-item clearfix', infinitescroll : item.infinitescroll, html: '<div class="pull-left m-left-sm"><span><div class="activity-icon small"><i class="fa fa-'+this.mapping[item.type]+'"></i></div><a href="/client/#'+item.client_id+'">'+item.client+'</a> - '+textlength(item.description,140)+'</span><br/><small class="text-muted"><i class="fa fa-clock-o"></i> '+moment(item.datecreated).fromNow()+'</small></div>' });
    }
    options['footer'] = '</div>';

    this.list(domid, output, options);
}

clientactivities.single = function(domid, items, options)
{
    options['wrapper'] = 'ul';

    output = [];
    if (items.length ==0) output.push({ 'class': 'list-group-item', html: 'Aucun activities' });
    else for (i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ 'class': 'list-group-item', infinitescroll : item.infinitescroll, html: '<b><i class="fa fa-'+this.mapping[item.type]+'"></i> <em>' + moment(item.datecreated).fromNow() + '</em></b> - ' + safe_html(item.description) });
    }
    this.list(domid, output, options);
}

clientactivities.form = function()
{
    return [ 
                { type: 'textarea', field: 'description', title: 'Descriptif' },
                { type: 'select', field: 'type', title: '', options: { 'note': "Note", 'email' : "Email", 'telephone' : "Telephone", 'rendezvous' : "Rendez-vous", 'passage' : "Passage" } }
            ];
}

clientactivities.me = 'clientactivities';
