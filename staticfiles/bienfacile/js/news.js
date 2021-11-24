news = new FeedObject('/json_news/');

news.all = function(domid, items, options)
{
    options['header'] = '';
    options['footer'] = '';
    options['wrapper'] = 'ul';
    options['wrapper_class'] = 'chat';
    var output = [];
    if (items.length ==0) output.push({ 'class': 'list-group-item', 'html': 'Pas de news!' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        if (item.photo)
            output.push({ 'class': 'right clearfix', infinitescroll : item.infinitescroll, html: '<a href="'+item.url+'"><span class="chat-img pull-right"><img src="'+item.photo+'" alt="'+item.agent+'"></span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+item.title+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(item.created_date).fromNow()+'</small></div><p'+(item.isnew?' class="newmsg"':'')+'>'+this.shorttext(item.id, 'description', 240)+'</p></div></a>' });
        else if (item.icon)
            output.push({ 'class': 'left clearfix', infinitescroll : item.infinitescroll, html: '<a href="'+item.url+'"><div class="activity-icon small"><i class="fa fa-'+item.icon+'"></i></div><span class="chat-img pull-right">none</span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+item.title+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(item.created_date).fromNow()+'</small></div><p'+(item.isnew?' class="newmsg"':'')+'>'+this.shorttext(item.id, 'description', 240)+'</p></div></a>' });
        else
            output.push({ 'class': 'left clearfix', infinitescroll : item.infinitescroll, html: '<a href="'+item.url+'"><div class="activity-icon small"><i class="fa fa-globe"></i></div><span class="chat-img pull-right">none</span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+item.title+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(item.created_date).fromNow()+'</small></div><p'+(item.isnew?' class="newmsg"':'')+'>'+this.shorttext(item.id, 'description', 240)+'</p></div></a>' });

    }
 
    this.list(domid, output, options);
}

news.me = 'news';

news.notifications = false;

news.notify = function(msg)
{
    notify('news', msg.url, msg.subject, textlength(msg.description, 140));
}