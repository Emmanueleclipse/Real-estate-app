function display_contactform(args)
{
	if (!args) return "Failed to supply arguments";
	var translations = { 'en' : { 'name' : 'Name', 'email' : 'Email', 'phone' : 'Telephone', 'notes' : "Message", 'wishto' : "You wish to", 'buy' : "Buy", 'sell': "Sell", 'price' : "Price", 'budget' : "Budget", 'send' : "Send" }};
	if (!args['language']) args['language'] = 'en';
	var words = translations[args['language']];
	var html = '<div class="field"><label>'+words['name']+'</label><input type="text" name="name" /></div>'+
				'<div class="field"><label>'+words['email']+'</label><input type="text" name="email" /></div>'+
				'<div class="field"><label>'+words['phone']+'</label><input type="text" name="phone" /></div>'+
				'<div class="field"><label>'+words['notes']+'</label><textarea rows="4" name="notes" /></textarea></div>';
	if (window.buysell) args['buysell'] = window.buysell;
	if (!args['buysell']) html += '<div class="field"><label>'+words['wishto']+'</label><input type="radio" name="buysell" value="buy" /> '+words['buy']+' <input type="radio" name="buysell" value="sell" /> '+words['sell']+'</div>';
	if (window.price) args['price'] = window.price;
	if (!args['price']) html += '<div class="field"><label>'+(args['buysell']=='sell'?words['price']:words['budget'])+'</label><input type="text" name="price" /></div>';
	for (var key in args) html += '<input type="hidden" name="'+key+'" value="'+args[key]+'">';

	return '<form id="contactform" action="#" onsubmit="submit_contactform();return false;" method="GET">'+"{% csrf_token %}"+html+'<span style="color:red"><div id="contactform_errors"></div></span><button type="submit">'+words['send']+'</button></form>';
}

function submit_contactform()
{
	var translations = { 'en' : { 'missingemailphone' : 'Please enter an email address or a telephone number', 'missing' : 'Please fill in the form so we can send it.', 'missingname' : "Please fill in your name, so we know who to ask for", 'missingagent' : "Nobody in form to send to", 'unknownagent' : "Contact form needs updating to new owner" }, 'fr' : { 'missingname' : "Merci de remplir votre nom", 'missingemailphone' : 'Merci de remplir un email ou numero telephone', 'missing' : "Pas assez d'info, merci de remplir la formulaire"} };
	var args = {}, fields = $( "form#contactform" ).serializeArray();
	for (var key in fields) { if (fields[key]['value'].length > 0) args[fields[key]['name']] = fields[key]['value']; }
//	alert(JSON.stringify(args));
	if (!args['language']) args['language'] = 'en';
	var words = translations[args['language']];
	var crossDomain = true; var dataType = 'jsonp';
    jQuery.ajax({ url: '{{ settings.SITE_URL }}/contactform/', cache: false, crossDomain: crossDomain, data: args, method: 'GET', async: false, dataType: 'html', context: document.body, timeout: 5000,
                success: function(a){ result = JSON.parse(a);
                	if (result["failed"] == true) $('#contactform_errors').html('<hr/>'+words[result['trans']]+'<hr/>');
                	else $('#contactform').html('<p>Thank you for getting in contact, '+result['name']+', we will get back to you as soon as possible.</p>');
                },
                error: function(xhr, textStatus, errorThrown){ $('#contactform').html(textStatus+' ('+errorThrown+'): '+JSON.stringify(xhr)); }
            });
    return false;
}
