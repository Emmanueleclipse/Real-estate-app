clientcontacts = new FeedObject('/json_contacts_client/');

clientcontacts.notfound = function(domid, phrase)
{
    result = [];
    if (!phrase || phrase == null) phrase = '';
    if (mobile = phrase.match(/0[6-7][ ]?\d\d[ ]?\d\d[ ]?\d\d[ ]?\d\d/)) { result.push("Portable: "+mobile[0]+"<input type=\"hidden\" name=\"telephone_type\" value=\"Portable\"><input type=\"hidden\" name=\"telephone\" value=\""+mobile[0]+"\">"); phrase = phrase.replace(mobile[0], '//'); }
    else if (phone = phrase.match(/\d\d \d\d \d\d \d\d \d\d/)) { result.push("<br/>Téléphone: "+phone[0]+"<input type=\"hidden\" name=\"telephone\" value=\""+phone[0]+"\">"); phrase = phrase.replace(phone[0], '//'); }
    if (phone = phrase.match(/\+[\d ]+\d/)) { result.push("<br/>Téléphone: "+phone[0]+"<input type=\"hidden\" name=\"telephone\" value=\""+phone[0]+"\">"); phrase = phrase.replace(phone[0], '//'); }
    if (email = phrase.match(/[\w.-]+@[\w.]+/)) { result.push("<br/>Email: "+email[0]+"<input type=\"hidden\" name=\"email\" value=\""+email[0]+"\">"); phrase = phrase.replace(email[0], '//'); }
    status = ''; phrase = '// '+phrase+' //';
    var i, len, titles = [' m ',' mr ',' mrs ',' mme ',' mlle ',' dr ',];
    for (len = titles.length, i=0; i<len; ++i)
    {
        pos = phrase.indexOf(titles[i])
        if (pos != -1) { phrase = phrase.replace(titles[i],''); result.push('<input type="hidden" name="status" value="'+titles[i].trim()+'">'); }
    }
    if (names = phrase.match(/[\w- ]+/))
    {
        var tmp = names[0].trim()
        var pos = tmp.lastIndexOf(' ');
        
        if (pos < 0) { forename = capitalise(tmp); surname = ''; }
        else { forename = capitalise(tmp.substring(0,pos).trim()); surname = capitalise(tmp.substring(pos).trim()); }
        phrase = phrase.replace(names[0], '//');
    }
    if (notes = phrase.match(/[\w]+[\w\d- ]+/)) { result.push("<br/>Notes: "+notes[0]+"<input type=\"hidden\" name=\"notes\" value=\""+notes[0]+"\">"); }

    result.push('<input type="hidden" name="forename" value="'+forename+'"><input type="hidden" name="surname" value="'+surname+'">');
    $(domid).html('<div class="client"><form method="POST" id="addclient" onSubmit="javascript:'+this.me+'.update(\'#addclient\'); '+this.me+'.resetfilter(\'#filter\'); return false;"><input type="hidden" name="csrfmiddlewaretoken" value="'+this.csrf+'"<i>'+capitalise(status)+'</i> '+forename+' <b>'+surname+'</b><hr/>'+result.join('<br>')+'<hr/><button type="submit" class="btn btn-sm btn-success"><i class="fa fa-edit fa-lg"></i> Enregistrer</button></form></div>');
}

clientcontacts.all = function(domid, items, options)
{
    options['isotope'] = true;
    var output = [], item, name;
    if (items.length ==0) { this.notfound(domid, this.search[domid]); return; }
    else for (i=0; i<items.length; i++)
    {
        item = items[i];
        contacts = { 'id' : item.id, 'client_id' : item.client_id, 'telephone' : item.telephone, 'email' : item.email, 'extras' : [ { 'icon': 'more', 'text' : 'Details', 'href' : '/client/#'+item.client_id } ] };
        name = (item.title && !item.forename?item.title+' ':'')+(item.forename?item.forename:'')+(item.surname?' '+item.surname:'');
        card = {
                    'title' : '<a href="/client/#'+item.client_id+'">'+name+'</a>',
                    'body' : (item.trash?item.trash:card_contactbar(contacts)),
                };
        output.push({ 'class' : 'card'+(item.trash?' trash':''), search : item.search, infinitescroll: item.infinitescroll, html: card_display(card) });
    }
    this.list(domid, output, options);

}


clientcontacts.single = function(domid, items, options)
{
    options['wrapper'] = 'ul';
    var output = [];
    if (items.length ==0) output.push({ 'class': 'list-group-item', html: 'Pas de contacts' });
    else for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        var phone = []; var mail = [];
        var actions = { 'Coordonnées': 'javascript:clientcontacts.modal(\'#modal\', { title : \'Modifier contact\', hidden: { id: #id# } });',
                         '+ Telephone': 'javascript:clientcontacts.modal(\'#modal\', { title : \'Nouveau téléphone\', form: \'form_telephone\', hidden: { id: #id# } });',
                         '+ Email': 'javascript:clientcontacts.modal(\'#modal\', { title : \'Nouveau email\', form: \'form_email\', hidden: { id: #id# } });',
                         'Supprimer': 'javascript:clientcontacts.modal_delete(\'#modal\', #id# );',
                    };
        if (item.telephone&&item.telephone.length>0)
            for (var j=0; j<item.telephone.length; j++) phone.push('<a href="javascript:clientcontacts.modal(\'#modal\', { title : \'Modifier téléphone\', form: \'form_telephone\', subobject: \'telephone\', hidden: { id: '+item.id+', telephone__id : '+item.telephone[j]['id']+' } });">'+item.telephone[j]['number']+(item.telephone[j]['type']?' <em>('+item.telephone[j]['type']+')</em>':'')+'</a>');
        if (item.email&&item.email.length>0)
            for (var j=0; j<item.email.length; j++) mail.push('<a href="javascript:clientcontacts.modal(\'#modal\', { title : \'Modifier email\', form: \'form_email\', subobject: \'email\', hidden: { id: '+item.id+', email__id : '+item.email[j]['id']+' } });">'+item.email[j]['email']+(item.email[j]['type']?' <em>('+item.email[j]['type']+')</em>':'')+'</a>');
        var name = (item.forename?item.forename:(item.title?item.title:''))+' '+(item.surname?item.surname:'')
        output.push({ 'class': 'list-group-item', infinitescroll: item.infinitescroll, html:
                        ''+divRow(
                        divCol(name,3)+
                        divCol(phone.join('<br/>')+'<br/>',3)+
                        divCol(mail.join('<br/>'),3)+
                        divCol(modifyButton('Action', actions, { '#id#': item.id }),3))+
                        (item.notes || item.language?divRow(divCol((item.language?'Langue: '+this.language_options[item.language]+'.&nbsp;':'')+(item.notes?'<em>'+item.notes+'</em>':''))):'')
                         });
    }
    this.list(domid, output, options);

}

clientcontacts.form = function()
{
    return [
                [
                [{ type: 'select', field: 'status', title: '', options: { 10: 'Monsieur', 20: 'Madame', 30: 'Mlle', 40: 'Dr', 50: 'Proff' } } ],
                    [{ type: 'input', field: 'forename', title: 'Prenom' }],
                    [{ type: 'input', field: 'surname', title: 'Nom famille' }],
                ],
                [
                    [{ type: 'select', field: 'language', title: '', options: this.language_options } ],
                   
                    [{ type: 'select', field: 'relationship', title: '', options: { 10: 'Partner', 20: 'Husband', 30: 'Wife', 40: 'Brother', 50: 'Sister', 60: 'Mother', 70: 'Father', 80: 'Cousin', 90: 'Friend', 100: 'Assistant',110: 'Personal Assistant',120: 'Property Manager',130: 'Cleaner', 999:  'Other' } } ],
                ],
                { type: 'textarea', field: 'notes', title: 'Notes' },
            ];
}

clientcontacts.form_telephone = function()
{
    return [
                [
                    [{ type: 'input', field: 'telephone__number', title: 'Numéro', required: true }],
                    [{ type: 'input', field: 'telephone__type', title: 'Commentaire' }],
                ],
            ];
}

clientcontacts.form_email = function()
{
    return [
                [
                    [{ type: 'input', field: 'email__email', title: 'Email', required: true }],
                    [{ type: 'input', field: 'email__type', title: 'Commentaire' }],
                    [{ type: 'boolean', field: 'email__reply_to', title: 'Principal' }],
                ],
            ];
}

clientcontacts.language_options = { 'fr': 'Francais', 'en': 'Anglais', 'it': 'Italien', 'ru': 'Russian', };

clientcontacts.me = 'clientcontacts';
