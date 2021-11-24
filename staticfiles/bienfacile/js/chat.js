
chat = new FeedObject('/json_chat/');

chat.single = function(domid, items, options)
{
    options['header'] = '';
    options['footer'] = '';
    options['wrapper'] = 'ul';
    options['wrapper_class'] = 'chat';
    var output = [];
    if (items.length ==0) output.push({ 'class': 'list-group-item', html: 'Trouvez quelqu\'un' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ 'class': (item.mine?'left':'right')+' clearfix', infinitescroll : item.infinitescroll, html: '<span class="chat-img pull-'+(item.mine?'left':'right')+'"><img src="'+(item.thumbnail?item.thumbnail:'')+'" alt="No photo"></span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+item.agent+' &gt; '+item.recipient+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(item.when).fromNow()+'</small></div><p'+(item.isnew?' class="newmsg"':'')+'>'+this.shorttext(item.id, 'message', 1024)+'</p></div>' });
    }
    this.list(domid, output, options);
}

chat.formbox = function()
{
    return [
                { type: 'input', field: 'message', title: 'Ditez quelque chose...', submit: true, required : true },
            ];
}

chat.form = function()
{
    return [
                { type: 'input', field: 'message', title: 'Ditez quelque chose...', required : true },
            ];
}

chat.me = 'chat';

listchat = new FeedObject('/json_listchat/');

listchat.all = function(domid, items, options)
{
    options['wrapper'] = 'ul';
    var output = [];
    if (items.length ==0) output.push({ 'class': 'list-group-item', html: 'Cliquez sur une colleague<p><u><a href="/agents/">Liste ici</a></u>' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
//        output.push({ 'class': ' clearfix', infinitescroll : item.infinitescroll, html: '<a href="javascript:chat.attach(\'#chat\', \'single\', { filter : {\'thread\' : '+item.agent_id+' } } ); chat.display();refresh(chat,2);chat.hidden={\'to_agent_id\' : \''+item.agent_id+'\'};chat.edit(\'#postchat\', { \'submit-inline\': true, \'hidden\': chat.hidden });unreadchat.update(null,{ \'agent_id\' : '+item.agent_id+' });"><span class="pull-left"><img width="64" height="64" src="'+(item.thumbnail?item.thumbnail:'')+'" alt="No photo" class="img-circle"></span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+item.agent+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(item.when).fromNow()+'</small>'+(item.unread?'&nbsp;<small class="chat-alert badge badge-danger">'+item.unread+'</small>':'')+'</div><hr/><div style="white-space: nowrap; overflow: hidden"><i>'+item.extract+'</i></div></div></a>' });
        output.push({ 'class': ' clearfix', infinitescroll : item.infinitescroll, html: '<a href="javascript:chat.storepush(\'last_chat\', { agent_id: '+item.agent_id+', agent: \''+item.agent+'\'},5);chat.attach(\'#chat\', \'single\', { filter : {\'thread\' : '+item.agent_id+' } } ); chat.display(); refresh(chat,2);chat.sethidden(\'to_agent_id\', \''+item.agent_id+'\');chat.edit(\'#postchat\', { \'submit-inline\': true, \'hidden\': chat.hidden });unreadchat.updatesilent(null,{ \'agent_id\' : '+item.agent_id+' }); nextslide();"><span class="pull-left"><img width="64" height="64" src="'+(item.thumbnail?item.thumbnail:'')+'" alt="No photo" class="img-circle"></span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+item.agent+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(item.when).fromNow()+'</small>'+(item.unread?'&nbsp;<small class="chat-alert badge badge-danger">'+item.unread+'</small>':'')+'</div><hr/><div style="white-space: nowrap; overflow: hidden"><i>'+item.extract+'</i></div></div></a>' });
    }
 
    this.list(domid, output, options);
}

listchat.me = 'listchat';

unreadchat = new FeedObject('/json_unreadchat/');


unreadchat.all = function(domid, items, options)
{
    var output = [], done = [];
    var last_chats = chat.retrieve('last_chat');
    output.push({ html: '<li><a href="/groupchat/"><span class="submenu-label">Agence</span></a></li>' });
    output.push({ html: '<li><a href="/chat/"><span class="submenu-label">Confr&egrave;res</span></a></li>' });
    if (items.length>1) for (var i=1; i<items.length; i++)
    {
        var item = items[i];
        done.push(item.agent_id);
        output.push({ html: '<li><a href="/chat/?agent='+item.agent_id+'"><span class="submenu-label">'+item.agent+'&nbsp;<small class="pull-right chat-alert badge badge-danger">'+item.total+'</small></span></a></li>' });
    }
    if (last_chats && last_chats.length>0) for (var i=0; i<last_chats.length; i++)
    {
        var last_chat = last_chats[i];
        if (!done.includes(last_chat.agent_id)) { output.push({ html: '<li><a href="/chat/?agent='+last_chat.agent_id+'"><span class="submenu-label">'+last_chat.agent+'</span></a></li>' }); done.push(last_chat.agent_id); }
    }
    this.list(domid, output, options);
}

unreadchat.totals = function(domid, items, options)
{
    var output = [];
    output.push({ html: items[0].total>0?'<small class="pull-right chat-alert badge badge-danger">'+items[0].total+'</small>':'' });

    this.list(domid, output, options);
}

unreadchat.me = 'unreadchat';

unreadchat.notifications = true;

unreadchat.notify = function(msg)
{
    if (msg.agent_id) notify('agentchat_'+msg.agent_id, '/chat/?agent='+msg.agent_id, msg.agent, msg.total+' message non lu');
}