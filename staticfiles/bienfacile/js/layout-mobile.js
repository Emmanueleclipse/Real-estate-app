function card_title(text,actions) { return '<h4>'+(text?text:'')+card_titleactions(actions)+'</h4>'; }

function contact_icons(icon) { icons = { 'telephone' : 'phone', 'edit' : 'edit', 'chat' : 'comment-o', 'mail' : 'envelope', 'more' : 'info-circle', 'sms' : 'mobile-phone', 'home' : 'home', 'web' : 'globe' }; return icons[icon]; }

function card_contactbutton(icon,text,href)
{
    return '<a class="btn btn-md btn-success" href="'+href+'"><i class="fa fa-'+contact_icons(icon)+'"></i><br/><span>'+text+'</span></a>';
}

function is_mobilenumber(number)
{
    var tmp = number.replace(/^[0+ ]+|\s+$/g,"");
    if (tmp > '5' && tmp < '8') return true;
    return false;
}

function card_contactbar(contact)
{
    var html = '<div class="btn-group" role="group" aria-label="...">', i;
    if (contact['object'] == 'contact') html += card_contactbutton('more', 'Details', '/client/#'+contact.client_id);
    if (contact.telephone) for (i =0; i < contact.telephone.length; i++) html += card_contactbutton('telephone', (contact.telephone[i]['type']?contact.telephone[i]['type']:'Appelle'), 'tel:'+contact.telephone[i]['number'])+(is_mobilenumber(contact.telephone[i]['number'])?card_contactbutton('sms', 'SMS', 'sms:'+contact.telephone[i]['number']):'');
    if (contact.email) for (i =0; i < contact.email.length; i++) html += card_contactbutton('mail', (contact.email[i]['type']?contact.email[i]['type']:'Email'), 'mailto:'+contact.email[i]['email']);
    if (contact.chat) html += card_contactbutton('chat', 'Chat', 'javascript:chat.modal(\'#modal\', { title : \'Envoyer message\', hidden: { to_agent_id: '+contact.chat+' } });');
//    html += card_contactbutton('more', 'Plus', '/agent/'+contact.id);
    if (contact.extras) for (i =0; i < contact.extras.length; i++) html += card_contactbutton(contact.extras[i].icon,contact.extras[i].text,contact.extras[i].href);

    return html+'</div>';
}

function card_titleactions(options) {
    var html = '';
    if (options && options.length > 0) for (var i = 0; i < options.length; i++) {
            html+= '<a class="pull-right" href="javascript:'+options[i]['action']+';">&nbsp;<i class="fa fa-'+contact_icons(options[i]['icon'])+'"></i>&nbsp;</a>';
    }
    return html;
}

function card_display(options)
{
    var html = '';
    if (options['title']) html += card_title(options['title'], options['titleactions']);
    html += options['body'];
    if (options['footer']) html += '<hr/>'+options['footer'];
    return html;
}
