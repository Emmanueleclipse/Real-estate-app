
/*! agents.js - Author: BienFacile, License: Bienfacile, more info: http://www.bienfacile.com/ */
agents=new FeedObject('/json_agents/');agents.me='agents';agents.all=function(a,b,c){c.isotope=true;var d=[];var e,f,g;for(i=0;i<b.length;i++){e=b[i];edit=(isadmin?' <a class="pull-right" href="javascript:agents.modal(\'#modal\', { title : \'Modifier agent\', hidden: { id: '+e.id+' } });">&nbsp;<i class="fa fa-edit"></i>&nbsp;</a>':'');chatbox=(e.isonline?' <a class="pull-right" href="javascript:chat.modal(\'#modal\', { title : \'Envoyer message\', hidden: { to_agent_id: '+e.id+' } });"><i class="fa fa-comment-o"></i></a>':'');f=(e.mobile?'Téléphone: '+e.mobile:' ');g=(e.email?'<a href="mailto:'+e.email+'"><i class="fa fa-envelope"></i></a> ':' ');d.push({search:e.search,infinitescroll:e.infinitescroll,html:'<h4>'+e.forename+' '+e.surname+edit+chatbox+'</h4><h5>'+g+f+'<br/><br/><a href="/agence#'+e.agency_id+'">'+e.agency+'</a></h5>'});}this.list(a,d,c);};agents.form=function(){return [{type:'input',field:'forename',title:'Forename'},{type:'input',field:'surname',title:'Surname'},{type:'input',field:'role',title:'Role'},{type:'input',field:'mobile',title:'Mobile'},{type:'input',field:'email',title:'Email'},{type:'boolean',field:'public',title:'Public'}];};