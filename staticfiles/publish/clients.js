
/*! clientactivities.js - Author: BienFacile, License: Bienfacile, more info: http://www.bienfacile.com/ */
clientactivities=new FeedObject('/json_recent_activities/');clientactivities.mapping={'note':'paperclip','email':'mail-reply','telephone':'phone','rendezvous':'car','passage':'building','web':'globe'};clientactivities.all=function(a,b,c){c.header='<div class="panel panel-default">';c.wrapper='ul';output=[];if(b.length==0)output.push({'class':'list-group-item',html:'Aucun activities'});else for(i=0;i<b.length;i++){var d=b[i];output.push({'class':'list-group-item clearfix',infinitescroll:d.infinitescroll,html:'<div class="pull-left m-left-sm"><span><div class="activity-icon small"><i class="fa fa-'+this.mapping[d.type]+'"></i></div><a href="/client/#'+d.client_id+'">'+d.client+'</a> - '+textlength(d.description,140)+'</span><br/><small class="text-muted"><i class="fa fa-clock-o"></i> '+moment(d.datecreated).fromNow()+'</small></div>'});}c.footer='</div>';this.list(a,output,c);};clientactivities.single=function(a,b,c){c.wrapper='ul';output=[];if(b.length==0)output.push({'class':'list-group-item',html:'Aucun activities'});else for(i=0;i<b.length;i++){var d=b[i];output.push({'class':'list-group-item',infinitescroll:d.infinitescroll,html:'<b><i class="fa fa-'+this.mapping[d.type]+'"></i> <em>'+moment(d.datecreated).fromNow()+'</em></b> - '+safe_html(d.description)});}this.list(a,output,c);};clientactivities.form=function(){return [{type:'textarea',field:'description',title:'Descriptif'},{type:'select',field:'type',title:'',options:{'note':"Note",'email':"Email",'telephone':"Telephone",'rendezvous':"Rendez-vous",'passage':"Passage"}}];};clientactivities.me='clientactivities';
/*! clientcontacts.js - Author: BienFacile, License: Bienfacile, more info: http://www.bienfacile.com/ */
clientcontacts=new FeedObject('/json_contacts_client/');clientcontacts.notfound=function(a,b){result=[];if(!b||b==null)b='';if(mobile=b.match(/0[6-7][ ]?\d\d[ ]?\d\d[ ]?\d\d[ ]?\d\d/)){result.push("Portable: "+mobile[0]+"<input type=\"hidden\" name=\"telephone_type\" value=\"Portable\"><input type=\"hidden\" name=\"telephone\" value=\""+mobile[0]+"\">");b=b.replace(mobile[0],'//');}else if(phone=b.match(/\d\d \d\d \d\d \d\d \d\d/)){result.push("<br/>Téléphone: "+phone[0]+"<input type=\"hidden\" name=\"telephone\" value=\""+phone[0]+"\">");b=b.replace(phone[0],'//');}if(phone=b.match(/\+[\d ]+\d/)){result.push("<br/>Téléphone: "+phone[0]+"<input type=\"hidden\" name=\"telephone\" value=\""+phone[0]+"\">");b=b.replace(phone[0],'//');}if(email=b.match(/[\w.-]+@[\w.]+/)){result.push("<br/>Email: "+email[0]+"<input type=\"hidden\" name=\"email\" value=\""+email[0]+"\">");b=b.replace(email[0],'//');}status='';b='// '+b+' //';var c,d,e=[' m ',' mr ',' mrs ',' mme ',' mlle ',' dr '];for(d=e.length,c=0;c<d;++c){g=b.indexOf(e[c]);if(g!=-1){b=b.replace(e[c],'');result.push('<input type="hidden" name="status" value="'+e[c].trim()+'">');}}if(names=b.match(/[\w- ]+/)){var f=names[0].trim();var g=f.lastIndexOf(' ');if(g<0){forename=capitalise(f);surname='';}else{forename=capitalise(f.substring(0,g).trim());surname=capitalise(f.substring(g).trim());}b=b.replace(names[0],'//');}if(notes=b.match(/[\w]+[\w\d- ]+/))result.push("<br/>Notes: "+notes[0]+"<input type=\"hidden\" name=\"notes\" value=\""+notes[0]+"\">");result.push('<input type="hidden" name="forename" value="'+forename+'"><input type="hidden" name="surname" value="'+surname+'">');$(a).html('<div class="client"><form method="POST" id="addclient" onSubmit="javascript:'+this.me+'.update(\'#addclient\'); '+this.me+'.resetfilter(\'#filter\'); return false;"><input type="hidden" name="csrfmiddlewaretoken" value="'+this.csrf+'"<i>'+capitalise(status)+'</i> '+forename+' <b>'+surname+'</b><hr/>'+result.join('<br>')+'<hr/><button type="submit" class="btn btn-sm btn-success"><i class="fa fa-edit fa-lg"></i> Enregistrer</button></form></div>');};clientcontacts.all=function(a,b,c){c.isotope=true;var d=[],e,f;if(b.length==0){this.notfound(a,this.search[a]);return;}else for(i=0;i<b.length;i++){e=b[i];contacts={'id':e.id,'client_id':e.client_id,'telephone':e.telephone,'email':e.email,'extras':[{'icon':'more','text':'Details','href':'/client/#'+e.client_id}]};f=(e.title&&!e.forename?e.title+' ':'')+(e.forename?e.forename:'')+(e.surname?' '+e.surname:'');card={'title':'<a href="/client/#'+e.client_id+'">'+f+'</a>','body':(e.trash?e.trash:card_contactbar(contacts))};d.push({'class':'card'+(e.trash?' trash':''),search:e.search,infinitescroll:e.infinitescroll,html:card_display(card)});}this.list(a,d,c);};clientcontacts.single=function(a,b,c){c.wrapper='ul';var d=[];if(b.length==0)d.push({'class':'list-group-item',html:'Pas de contacts'});else for(var e=0;e<b.length;e++){var f=b[e];var g=[];var h=[];var i={'Coordonnées':'javascript:clientcontacts.modal(\'#modal\', { title : \'Modifier contact\', hidden: { id: #id# } });','+ Telephone':'javascript:clientcontacts.modal(\'#modal\', { title : \'Nouveau téléphone\', form: \'form_telephone\', hidden: { id: #id# } });','+ Email':'javascript:clientcontacts.modal(\'#modal\', { title : \'Nouveau email\', form: \'form_email\', hidden: { id: #id# } });','Supprimer':'javascript:clientcontacts.modal_delete(\'#modal\', #id# );'};if(f.telephone&&f.telephone.length>0)for(var j=0;j<f.telephone.length;j++)g.push('<a href="javascript:clientcontacts.modal(\'#modal\', { title : \'Modifier téléphone\', form: \'form_telephone\', subobject: \'telephone\', hidden: { id: '+f.id+', telephone__id : '+f.telephone[j].id+' } });">'+f.telephone[j].number+(f.telephone[j].type?' <em>('+f.telephone[j].type+')</em>':'')+'</a>');if(f.email&&f.email.length>0)for(var j=0;j<f.email.length;j++)h.push('<a href="javascript:clientcontacts.modal(\'#modal\', { title : \'Modifier email\', form: \'form_email\', subobject: \'email\', hidden: { id: '+f.id+', email__id : '+f.email[j].id+' } });">'+f.email[j].email+(f.email[j].type?' <em>('+f.email[j].type+')</em>':'')+'</a>');var k=(f.forename?f.forename:(f.title?f.title:''))+' '+(f.surname?f.surname:'');d.push({'class':'list-group-item',infinitescroll:f.infinitescroll,html:''+divRow(divCol(k,3)+divCol(g.join('<br/>')+'<br/>',3)+divCol(h.join('<br/>'),3)+divCol(modifyButton('Action',i,{'#id#':f.id}),3))+(f.notes||f.language?divRow(divCol((f.language?'Langue: '+this.language_options[f.language]+'.&nbsp;':'')+(f.notes?'<em>'+f.notes+'</em>':''))):'')});}this.list(a,d,c);};clientcontacts.form=function(){return [[[{type:'select',field:'status',title:'',options:{10:'Monsieur',20:'Madame',30:'Mlle',40:'Dr',50:'Proff'}}],[{type:'input',field:'forename',title:'Prenom'}],[{type:'input',field:'surname',title:'Nom famille'}]],[[{type:'select',field:'language',title:'',options:this.language_options}],[{type:'select',field:'relationship',title:'',options:{10:'Partner',20:'Husband',30:'Wife',40:'Brother',50:'Sister',60:'Mother',70:'Father',80:'Cousin',90:'Friend',100:'Assistant',110:'Personal Assistant',120:'Property Manager',130:'Cleaner',999:'Other'}}]],{type:'textarea',field:'notes',title:'Notes'}];};clientcontacts.form_telephone=function(){return [[[{type:'input',field:'telephone__number',title:'Numéro',required:true}],[{type:'input',field:'telephone__type',title:'Commentaire'}]]];};clientcontacts.form_email=function(){return [[[{type:'input',field:'email__email',title:'Email',required:true}],[{type:'input',field:'email__type',title:'Commentaire'}],[{type:'boolean',field:'email__reply_to',title:'Principal'}]]];};clientcontacts.language_options={'fr':'Francais','en':'Anglais','it':'Italien','ru':'Russian'};clientcontacts.me='clientcontacts';