
todo = new FeedObject('/json_todo/');

todo.postfilter = function(items)
{
    expires = moment().format('YYYY-MM-DD'); // remove any completed before this calendar day
    results = [];
    for (item in items)
    {
        if (!items[item].completed_date) { items[item].completed = false; results.push(items[item]); }
        else if (items[item].completed_date >= expires) { items[item].completed = true; results.push(items[item]); }
    }
    return results;
}

todo.all = function(domid, items, options)
{
    options['header'] = '<div class="panel panel-default">';
    options['footer'] = '</div">';
    options['wrapper'] = 'ul';
    var output = [];
    if (items.length ==0) output.push({ 'class': 'list-group-item', 'html': 'Rien a faire pour maintenant' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        title = item.completed_date?'<strike>'+item.title+'</strike>':item.title;
        output.push({ 'class': 'list-group-item clearfix', 'infinitescroll' : item.infinitescroll, 'html': '<div class="pull-left m-left-sm"><span><b>'+(item.for_client?'<em><a href="/client/#'+String(item.for_client)+'">'+item.client+'</a></em> - ':'')+"<a href=\"javascript:todo.modal('#modal', { title : 'Modifier tache', hidden: { id: "+item.id+" } });\">"+title+'</a></b></span>'+(item.description?'<br/>'+textlength(item.description,140):'')+(item.due_date && !item.completed_date?'<br/><small class="text-muted"><i class="fa fa-clock-o"></i> '+this.renderdays(item.due_date)+'</small>':'')+(item.mine?'':'<br/>('+myagency.staff(item.assigned_to)+')')+'</div>' });
    }
 
    this.list(domid, output, options);
}

todo.single = function(domid, items, options)
{

    options['wrapper'] = 'ul';
    var output = [];
    if (items.length ==0) output.push({ 'class': 'list-group-item', 'html': 'Rien a faire pour maintenant' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        var title = item.completed_date?'<strike>'+item.title+'</strike>':item.title;
        output.push({ 'class': 'list-group-item', 'infinitescroll' : item.infinitescroll, 'html': "<b><a href=\"javascript:todo.modal('#modal', { title : 'Modifier tache', hidden: { id: "+item.id+" } });\">"+title+'</a></b> <em>' + (item.due_date?this.renderdays(item.due_date):'') + '</em>' + (item.description?' - '+escapeHtml(item.description):'')+(item.mine?'':'<br/>('+myagency.staff(item.assigned_to)+')') });
    }
    this.list(domid, output, options);

}

todo.form = function()
{
    return [
                { type: 'input', field: 'title', title: 'Titre', required: true },
                { type: 'textarea', field: 'description', title: 'Descriptif' },
                { type: 'input', field: 'tags', title: 'Tags' },
                [
                    [
                        { type: 'date', field: 'due_date', title: 'À faire avant' }
                    ],
                    [
                        { type: 'select2', field: 'for_client', title: 'Client', options: clients.options('name') },
                        { type: 'select2', field: 'assigned_to', title: 'Responsable', options: myagency.options('fullname') },
                        { type: 'boolean', field: 'completed', title: 'terminé' },
                    ]
                ]
            ];
}
todo.passthru = ['for_client'];

todo.markcomplete = function()
{
    return [
                { type: 'boolean', field: 'completed_date', title: '' },
            ];
}

todo.me = 'todo';
