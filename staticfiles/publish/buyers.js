
/*! buyers.js - Author: BienFacile, License: Bienfacile, more info: http://www.bienfacile.com/ */
buyers=new FeedObject('/json_buyers/');buyers.me='buyers';buyers.all=function(a,b,c){c.isotope=true;var d=[],e,f,g,h="javascript:buyers.updatesilent(null,{'togglelock' : {} });buyers.display();";for(var i=0;i<b.length;i++){e=b[i];if(e.hot)g=staticimage('locked.png');else g=staticimage('unlocked.png');;f=e.last_contact?moment(e.last_contact).fromNow():'Jamais contacté';card={'title':'<a href="/client/#'+e.client_id+'">'+(e.budget?'&euro;'+numberWithCommas(e.budget)+' - ':'')+e.what+'</a>'+'<a class="pull-right" href="'+h.replace("{}",e.client_id)+'">'+g+'<a>','body':this.readmore(e.description,'/client/#'+e.client_id)+(e.tags&&e.tags.length>0?'<hr/>'+this.taglist(e.tags):''),'footer':f+' '+e.who};d.push({search:e.search,infinitescroll:e.infinitescroll,html:card_display(card)});}this.list(a,d,c);};buyers.single=function(a,b,c){c.wrapper='panel';var d=[];for(var e=0;e<b.length;e++){var f=b[e];d.push({search:f.search,infinitescroll:f.infinitescroll,html:panelTop('Recherche '+f.what+(f.budget?' - &euro;'+numberWithCommas(f.budget):''),{'Modifier':'javascript:buyers.modal(\'#modal\', { title : \'Modifier recherche\', hidden: { id: '+f.id+' } });','Supprimer':'javascript:buyers.modal_delete(\'#modal\',  '+f.id+');'})+panelBody('<a href="javascript:buyers.modal(\'#modal\', { title : \'Modifier recherche\', hidden: { id: '+f.id+' } });">'+divRow(divCol(safe_html(f.description)))+'<hr/>'+divRow(divCol(this.taglist(f.tags,false,'btn-default btn-sm'),10)+divCol(moment(f.date_created).format("MMM Do YYYY"),2))+'</a>')});}this.list(a,d,c);};buyers.form=function(){return [[[{type:'select',field:'what',title:'',options:{'appartement':'Appartement','villa':'Villa','commerce':'Commerce','terrain':'Terrain','garage':'Garage'},'default':'appartement'}],[{type:'input',field:'budget',title:'Budget'}]],[[{type:'input',field:'tags',title:'Tags'}]],{type:'textarea',field:'description',title:'Notes'}];};buyers.trash=["Achet&eacute; avec moi","Achet&eacute; avec un autre agence","Achet&eacute; par un particulier","N'achete plus dans cette region","N'achete plus de tout","Pas serieux"];