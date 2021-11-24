groupchat = new FeedObject('/json_groupchat/');

groupchat.all = function(domid, items, options)
{
    options['header'] = '';
    options['footer'] = '';
    options['wrapper'] = 'ul';
    options['wrapper_class'] = 'chat';
    var output = [];
    if (items.length ==0) output.push({ 'class': 'list-group-item', 'html': 'Ditez quelque chose!' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ 'class': (item.mine?'left':'right')+' clearfix', 'infinitescroll' : item.infinitescroll, 'html': '<span class="chat-img pull-'+(item.mine?'left':'right')+'"><img src="'+(item.thumbnail?item.thumbnail:'')+'" alt="No photo"></span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+item.agent+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(item.when).fromNow()+'</small></div><p'+(item.isnew?' class="newmsg"':'')+'>'+this.shorttext(item.id, 'message', 240)+'</p></div>' });
    }
 
    this.list(domid, output, options);
}

groupchat.form = function()
{
    return [
                { type: 'input', field: 'message', title: 'Ditez quelque chose...', submit: true },
            ];
}

groupchat.me = 'groupchat';

groupchat.notifications = true;

groupchat.notify = function(msg)
{
    notify('groupchat', '/groupchat/', 'Group message from '+msg.agent, textlength(msg.message, 240));
}