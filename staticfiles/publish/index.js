
/*! myagency.js - Author: BienFacile, License: Bienfacile, more info: http://www.bienfacile.com/ */
myagency=new FeedObject('/json_monagence/');myagency.load(false);myagency.staff=function(a){var b=this.getdata(a);return this.fullname(b);};myagency.me='myagency';
/*! groupchat.js - Author: BienFacile, License: Bienfacile, more info: http://www.bienfacile.com/ */
groupchat=new FeedObject('/json_groupchat/');groupchat.all=function(a,b,c){c.header='';c.footer='';c.wrapper='ul';c.wrapper_class='chat';var d=[];if(b.length==0)d.push({'class':'list-group-item','html':'Ditez quelque chose!'});else for(var e=0;e<b.length;e++){var f=b[e];d.push({'class':(f.mine?'left':'right')+' clearfix','infinitescroll':f.infinitescroll,'html':'<span class="chat-img pull-'+(f.mine?'left':'right')+'"><img src="'+(f.thumbnail?f.thumbnail:'')+'" alt="No photo"></span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+f.agent+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(f.when).fromNow()+'</small></div><p'+(f.isnew?' class="newmsg"':'')+'>'+this.shorttext(f.id,'message',240)+'</p></div>'});}this.list(a,d,c);};groupchat.form=function(){return [{type:'input',field:'message',title:'Ditez quelque chose...',submit:true}];};groupchat.me='groupchat';groupchat.notifications=true;groupchat.notify=function(a){notify('groupchat','/groupchat/','Group message from '+a.agent,textlength(a.message,240));};
/*! news.js - Author: BienFacile, License: Bienfacile, more info: http://www.bienfacile.com/ */
news=new FeedObject('/json_news/');news.all=function(a,b,c){c.header='';c.footer='';c.wrapper='ul';c.wrapper_class='chat';var d=[];if(b.length==0)d.push({'class':'list-group-item','html':'Pas de news!'});else for(var e=0;e<b.length;e++){var f=b[e];if(f.photo)d.push({'class':'right clearfix',infinitescroll:f.infinitescroll,html:'<a href="'+f.url+'"><span class="chat-img pull-right"><img src="'+f.photo+'" alt="'+f.agent+'"></span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+f.title+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(f.created_date).fromNow()+'</small></div><p'+(f.isnew?' class="newmsg"':'')+'>'+this.shorttext(f.id,'description',240)+'</p></div></a>'});else if(f.icon)d.push({'class':'left clearfix',infinitescroll:f.infinitescroll,html:'<a href="'+f.url+'"><div class="activity-icon small"><i class="fa fa-'+f.icon+'"></i></div><span class="chat-img pull-right">none</span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+f.title+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(f.created_date).fromNow()+'</small></div><p'+(f.isnew?' class="newmsg"':'')+'>'+this.shorttext(f.id,'description',240)+'</p></div></a>'});else d.push({'class':'left clearfix',infinitescroll:f.infinitescroll,html:'<a href="'+f.url+'"><div class="activity-icon small"><i class="fa fa-globe"></i></div><span class="chat-img pull-right">none</span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">'+f.title+'</strong><small class="pull-right text-muted"><i class="fa fa-clock-o"></i> '+moment(f.created_date).fromNow()+'</small></div><p'+(f.isnew?' class="newmsg"':'')+'>'+this.shorttext(f.id,'description',240)+'</p></div></a>'});}this.list(a,d,c);};news.me='news';news.notifications=false;news.notify=function(a){notify('news',a.url,a.subject,textlength(a.description,140));};