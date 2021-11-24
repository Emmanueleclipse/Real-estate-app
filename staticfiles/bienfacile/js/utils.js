/* Extract a GET parameter from the query string */
function getQueryStringValue (key) {  
  return decodeURIComponent(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));  
}

function staticimage(name)
{
    return '<img src="'+staticimageurl+name+'"/>';
}
/* Layout functions */

function panelTop(title,actions)
{
    var html = '<div class="panel-heading">'+title;
    if (actions)
    {
        html += '<div class="btn-group pull-right"><button class="btn btn-primary btn-xs dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="caret"></span><span class="sr-only">Toggle Dropdown</span></button><ul class="dropdown-menu">';
        if (actions) for (var i in actions) if (i == '') html += '<li><hr/></li>'; else html += '<li><a href="'+actions[i]+'">'+i+'</a></li>';
        html += '</ul></div>';
    }
    html += '</div>';
    return html;
}
function panelBody(html) { return '<div class="panel-body">'+html+'</div>'; }
function divRow(html) { return '<div class="row">'+html+'</div>';}
function divCol(html,num) { return '<div class="mx-auto col-md-'+(num?num:12)+'">'+html+'</div>'; }
function addNewButton(title,action) { return '<button class="btn btn-xs btn-default" type="button"><i class="fa fa-plus"></i> '+title+'</button>'; }

function modifyButton(title, actions, replace)
{
    var html = '<div class="btn-group pull-right"><button class="btn btn-default dropdown-toggle" data-toggle="dropdown">Action <span class="caret"></span></button><ul class="dropdown-menu">';
    for (var i in actions)
        html += '<li><a href="'+actions[i]+'">'+i+'</a></li>';
    html += '</ul></div>';
    
    if (replace) for (var i in replace) { html = replaceAll(html,i, replace[i]); }
    return html;
}

function concat_cells(args)
{
    var output = '';
    for (var i=0; i<args.cells.length; i++)
        output = output + args.cell_open + (args.cells[i]?args.cells[i]:'') + args.cell_close;
    return output;
}

/* String and text formatting */

function escapeRegExp(str) {
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}
function replaceAll(str, find, replace) {
  return str.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}

var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
  };

function escapeHtml(string) {
	return String(string).replace(/[&<>"'\/]/g, function (s) {
		return entityMap[s];
    });
}

function strip_tags(input, allowed) {

    allowed = (((allowed || '') + '')
    .toLowerCase()
    .match(/<[a-z][a-z0-9]*>/g) || [])
    .join(''); // making sure the allowed arg is a string containing only tags in lowercase (<a><b><c>)
    var tags = /<\/?([a-z][a-z0-9]*)\b[^>]*>/gi,
    commentsAndPhpTags = /<!--[\s\S]*?-->|<\?(?:php)?[\s\S]*?\?>/gi;
    return input.replace(commentsAndPhpTags, '')
    .replace(tags, function($0, $1) {
    return allowed.indexOf('<' + $1.toLowerCase() + '>') > -1 ? $0 : '';
    });
}

function safe_html(input)
{
    return strip_tags(input, ['<a>','<br/>','<p>','<b>','<i>']);
}

function escapequotes(a)
{
    return a.replace('"', '&quot;').replace("'", "\\'");
}

function textlength(string, length) {
    if (string == null) return '';
    if (string.length <= length) return string;
    string = string.substring(0,length);
    var end = string.lastIndexOf(' ');
    if (end) string = string.substring(0,end);
    return string+'...';
}

function monthname(month)
{
    var monthNames = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    return monthNames[month];
}

function numberWithCommas(x) { if (x) return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); return x; }
function capitalise(phrase) { return phrase.charAt(0).toUpperCase() + phrase.substring(1); }

function showPrice(x) { if (!x || x== '') return null; return '&euro;' + numberWithCommas(Math.round(x)); }

function extractkeywords(phrase)
{
    if (!phrase || phrase == null || phrase.length==0) return false;
    phrase = phrase.toLowerCase();
    if (phrase.indexOf(' ')>0) return phrase.split(' ');
    return [ phrase ];
}

function searchstring(search,keywords)
{
    if (!search  || !keywords) return false;
    var ignore = ['m', 'mme', 'mr', 'mlle', 'mm']
    var pos = 0, len = keywords.length, found = null;
    for(var i = 0; i < len; i++){
        if (keywords[i] == '' || ignore.indexOf(keywords[i]) != -1) continue;
        found = search.indexOf(keywords[i]);
        if (found == -1) return false;
        else if (found < pos) return false;
        else pos = found;
    }
    return true;
}

function dynamicSort(property) {
    var sortOrder = 1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
}

function attr(key, value)
{
    if (!value || value.length ==0) return '';
    if (typeof value === 'string') return ' '+key+'="'+value+'"';
    return ' '+key+'="'+value.join(' ')+'"';
}

/* DOM functions */

function get_clientid()
{
    return parseInt(window.location.hash.substring(1));
}


function selectoption(id,value)
{
    $('#'+id+' option').removeAttr('selected').filter('[value='+value+']').attr('selected', true);
}

function refresh(command, timeout)
{
    setInterval(function(){ command.load(); }, timeout*1000);
}

function notify(tag, url, title, message, icon)
{
    if (Notification.permission=="granted")
    {
        var options={ tag: (tag?tag:'bienfacile')};
        if (message) options.body = message;
        var noti= new Notification((title?title:null),options);
        noti.onclick = function(event) { window.location.href=url; }
    }
}

/* For mobile */
function nextslide()
{
  if (typeof window.mySwiper !== 'undefined') { window.mySwiper.slideNext(); }
}

function forcepagereload()
{
    $('#pagetop').html('<div class="alert alert-danger" role="alert"><a href="#" class="alert-link">Server problem. Refreshing page...</a></div><script> setTimeout(location.reload(), 5000); </script>');
}

function linkify(inputText) {

    if (!inputText || inputText == '') return '';
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    //URLs starting with http://, https://, or ftp://
    replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(replacePattern1, '<a href="$1" target="_blank">$1</a>');

    //URLs starting with "www." (without // before it, or it'd re-link the ones done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(replacePattern2, '$1<a href="http://$2" target="_blank">$2</a>');

    //Change email addresses to mailto:: links.
    replacePattern3 = /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText = replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');

    return replacedText;
}

/* FeedObject for taking and displaying JSON feeds */
/*
String.prototype.hashCode = function(){
    var hash = 0, char = null;
    if (this.length == 0) return hash;
    for (var i = 0; i < this.length; i++)
    {
        char = this.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
}
*/

/* For unique hash */

function hashCode (target){
    var hash = 0, char = null;
    if (target == null || target.length == 0) return hash;
    for (var i = 0; i < target.length; i++)
    {
        char = target.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
}

/* Main feed object */

FeedObject = function(feedurl) {
        this.data = false;
        this.isnew = [];
        this.notifications = false;
        this.data_index = false;
        this.url = feedurl;
        this.pager = false;
        this.perpage = 20;
        this.callbackrender = {};
        this.search = {};
        this.filters = {};
        this.hidden = {};
        this.locked = false;
        this.sortby = {};
        this.ranges = {};
        var self=this;

        this.refresh = function(timeout) {
            setInterval(function(){ self.load(); return; }, timeout*1000);
        }

        this.postfilter = function(a)
        {
            return a;
        }

        this.updatedata = function(a) {
            var hash = hashCode(JSON.stringify(a));
            if (this.data && this.hash == hash) return false;
            if (this.data)
            {
                this.setindex();
                for (var i=0; i < a.length; i++)
                {
                    a[i].hash = hashCode(JSON.stringify(a[i]));
                    a[i]['modified'] = false;
                    if (this.data_index[a[i].id] == null) { this.isnew.push(a[i].id); a[i].isnew = true; }
                    else { a[i].isnew = false; if (this.data[this.data_index[a[i].id]].hash != a[i].hash) a[i].modified = true; }
                    if (this.notifications && (a[i].isnew || a[i].modified)) this.notify(a[i]);
                }
            }
            else
            {
                for (var i=0; i < a.length; i++)
                {
                    a[i].hash = hashCode(JSON.stringify(a[i])); a[i]['isnew'] = false; a[i]['modified'] = false;
                }
            }
            this.data_index = false;
            a = this.postfilter(a);
            this.data = a;
            this.hash = hash;
            this.total = this.data.length;
            return true;
        }

        this.notify = function(a) { return false; }

        this.load = function(display) {
            if (this.url[0] == '/') { var crossDomain = false; var dataType = 'json'; } else { var crossDomain = true; var dataType = 'jsonp'; }
            jQuery.ajax({ url: this.url, cache: false, crossDomain: crossDomain, async: true, dataType: dataType, context: this, jsonp: 'callback', timeout: 5000,
//            jQuery.ajax({ url: this.url, cache: false, crossDomain: true, async: false, dataType: 'jsonp', jsonp: "callback", context: this,

                success: function(a){
                    if (this.updatedata(a) && display!==false) this.display();
               },
                error: function(xhr, textStatus, errorThrown){
                    if (DEBUGPAGE) alert(textStatus+' ('+errorThrown+'): '+JSON.stringify(xhr));
                    forcepagereload();
                }
            });
        }

        this.syncload = function() {
            if (this.url[0] == '/') { var crossDomain = false; var dataType = 'json'; } else { var crossDomain = true; var dataType = 'jsonp'; }
            jQuery.ajax({ url: this.url, cache: false, crossDomain: crossDomain, async: false, dataType: dataType, context: this, timeout: 5000,
                success: function(a){ this.updatedata(a); },
                error: function(xhr, textStatus, errorThrown){
                    if (DEBUGPAGE) alert(textStatus+' ('+errorThrown+'): '+JSON.stringify(xhr));
                    forcepagereload();
                }
            });
            console.log("loaded for "+this.me)
        }

        this.find_required_fields = function(arr, result) {
            for (var i=0; i<arr.length; i++)
            {
                if (Array.isArray(arr[i]))
                {
                    result.concat(this.find_required_fields(arr[i],result));
                }
                else if (arr[i]['required'] == true) result.push([arr[i]['field'],arr[i]['title']]);
            }
            return result;
        }

        this.update = function(formid, data2, data3, data4) {
            if (!window.csrf) { alert("Missing CSRF token"); return false; }
            var data1 = { 'csrfmiddlewaretoken' : csrf };
            if (formid)
            {
                var tmp = $(formid).serializeArray();
                for (var i=0; i<tmp.length; i++) data1[tmp[i]['name']]=tmp[i]['value'];
            }
            data = Object.assign({},data1, (data2?data2:null), (data3?data3:null), (data4?data4:null), this.hidden);
           // Check for required fields
            errors = [];
            if (data['edit'])
            {
                required = this.find_required_fields(this[data['edit']](),[]);
                if (required.length > 0) for (var i=0; i < required.length; i++)
                {
                    if (!data[required[i][0]]) errors.push(required[i][1]+' est requis');
                }
                if (errors.length >0) { $(formid+'_errors').html(errors.join('<br/>')); return false; }
            }
            if (formid) document.getElementById(formid.substring(1)).reset();
//            jQuery.ajax({ url: this.url, cache: false, crossDomain: true, async: false, dataType: 'jsonp', jsonp: "callback", context: this,
            if (this.url[0] != '/') { alert("jsonp does not support POST"); return false; }
            jQuery.ajax({ url: this.url, cache: false, crossDomain: false, async: true, dataType: 'json', method: 'POST', data: data, context: this,jsonp: 'callback',

                success: function(a){
                    this.updatedata(a);
                    this.display();
               },
                error: function(xhr, textStatus, errorThrown){
                    if (DEBUGPAGE) alert(textStatus+': '+JSON.parse(String(xhr.responseText)['error']));
                    forcepagereload();
                }
            });
            return true;
        }

        this.updatesilent = function(formid, data2, data3, data4) {
            success = this.update(formid, data2, data3, data4);
            return;
        }

        this.attach = function(domid, func, options) { this.callbackrender[domid] = [func, options]; }

        this.display = function() {
            if (!this.data) { this.load(); return; }
            for (var domid in this.callbackrender)
            {
                this.display_continue(domid, 0);
            }
        }

        this.display_continue = function(domid, offset)
        {
            if (!offset) offset=0;
            var func = this.callbackrender[domid][0];
            var opts = this.callbackrender[domid][1];
            opts['start'] = offset;
            opts['infiniteid'] = domid+'scroll';
            opts['listid'] = domid+'List';
            opts['list-element'] = opts['listid'].substring(1);
            var perpage = opts['perpage']?opts['perpage']:this.perpage;
            var finish = opts['max']&&opts['max']<this.total?opts['max']:this.total;
            var shown = 0;
            var items = [], item = null, filterkeywords = null;
            var filter = false; var searched = true;
            var filters = opts['filter'];
            if (domid in this.filters) { filters = Object.assign({}, this.filters[domid],opts['filter']); } 
            while (offset < finish && shown < perpage)
            {
                item = this.data[offset];
                filter = false;
                if (filters) // deal with simple key / value field filters
                {
                    for (var key in filters)
                    {
                        if (typeof filters[key] === 'string' || typeof filters[key] === 'number') { if (item[key] != filters[key]) filter = true; break; }
                        else if (typeof filters[key] === 'object' && filters[key].length > 0) { if (filters[key].indexOf(item[key]) < 0) filter = true; break; }
                        else alert("Error with data type");
                    }
                }
                if (domid in this.ranges)
                {
                    for (var key in this.ranges[domid])
                    {
                        if (this.ranges[domid][key]['min'] && item[key] < this.ranges[domid][key]['min']) { filter = true; break; }
                        if (this.ranges[domid][key]['max'] && item[key] > this.ranges[domid][key]['max']) { filter = true; break; }
                    }
                }
                if (!filter) // if we survive the basic filters, see if we need to filter by search phrase
                {
                    searched = true;
                    if (this.search[domid])
                    {
                        filterkeywords = extractkeywords(this.search[domid]);
                        if (filterkeywords && !searchstring(item.search,filterkeywords)) searched = false;
                    }
                    if (searched)
                    {
                        shown+=1;
                        item.infinitescroll = (shown == perpage?true:false);
                        items.push(item);
                    }
                }
                offset+=1;
            }
            opts['offset'] = offset; opts['shown'] = shown;
            this[func](domid, items, opts);
        }

        this.notfound = function(domid, phrase) {
            $(domid).html("&nbsp;Aucun resultat pour '"+phrase+"'");
        }

        /* Attach a search box to a list */
        this.attachfilter = function(domid, target_domid) {
            var self = this.me;
            document.getElementById(domid.substring(1)).onkeyup = function(){ window[self].filteron(target_domid, this.value); }
        }

        this.attachmenufilter = function(domid, target_domid) {
            var self = this.me, newfilter = function(){ window[self].menufilter(target_domid, this.value); };
            document.getElementById(domid.substring(1)).addEventListener("keyup", newfilter, true);
        }

        this.resetfilter = function(domid) {
            document.getElementById(domid.substring(1)).value='';
        }

        this.menufilter = function(domid, value) {
            if (!this.data) this.syncload();
            this.search[domid] = value;
//            filterkeywords = extractkeywords(this.search[domid]);
//                        if (filterkeywords && !searchstring(item.search,filterkeywords)) searched = false;

            this.display_continue(domid, 0);
        }

        this.filter = function(domid, key, value) {
            if (!(domid in this.filters)) this.filters[domid] = {};
            this.filters[domid][key] = value;
            this.display_continue(domid, 0);
        }

        this.checktoggle = function(key,value) { return key !== value; }

        this.togglefilter = function(domid, key, value) {
            if (!(domid in this.filters)) this.filters[domid] = {};
            if (!(key in this.filters[domid])) newfilter = [];
            else if (typeof this.filters[domid][key] === 'string' || typeof this.filters[domid][key] === 'number') newfilter = [ this.filters[domid][key] ]; else newfilter = this.filters[domid][key];
            if (typeof value === 'string' || typeof value === 'number') value = [ value ];
            for (var i=0; i<value.length;i++)
            {
                if (newfilter.indexOf(value[i]) != -1) newfilter = newfilter.splice(newfilter.indexOf(value[i]));
                else newfilter.push(value[i]);
            }
            if (newfilter.length>0) this.filters[domid][key] = newfilter; else delete this.filters[domid][key];
            this.display_continue(domid, 0);
        }

        this.dynamicSort = function(property) {
            var sortOrder = 1;
            if(property[0] === "-") { sortOrder = -1; property = property.substr(1); }
            return function (a,b) {
                var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
                return result * sortOrder;
            }
        }

        this.sortby = function(domid, key){
            if (domid in this.sortby && this.sortby[domid] == key) key = (key[0]=='-'?key.substr(1):'-'+key);
            this.data = this.data.sort(this.dynamicSort(key));
            this.sortby[domid] = key;
            this.display_continue(domid, 0);
        }

        this.setrange = function(domid, key, min, max) {
            if (!(domid in this.ranges)) this.ranges[domid] = {};
            this.ranges[domid][key] = { 'min' : min, 'max' : max };
            this.display_continue(domid, 0);
        }

        /* Function: filteron - take a search phrase, and hide elements that do not match. If the new search phrase is shorter, then redisplay from scratch */
        this.filteron = function(domid, phrase) {
            var node = domid+'List';
            var filterkeywords = extractkeywords(phrase);
            var isoyes = $(node).data('isotope')?true:false;
            if (!filterkeywords) { delete(this.search[domid]); this.display_continue(domid, 0); return; }
            if (!this.search[domid] || phrase.length > this.search[domid].length)
            {
                if (isoyes) var elems = $(node).isotope('getItemElements');
                else
                {
                    var tmp = document.getElementById(node.substr(1));
                    var elems = tmp.getElementsByClassName(domid.substr(1)+'Item');
                }

                var numelems = elems.length;
                var found = 0;
                if (numelems == 0) { this.notfound(domid, phrase); return; }
                for (var j=0; j<numelems; j++)
                {
                    if (!searchstring(elems[j].getAttribute('search'),filterkeywords)) $(elems[j]).hide();
                    else found++;
                }
                this.search[domid] = phrase;
                if (isoyes) $(node).isotope('layout');
            }
            else if (this.search[domid] && phrase.length < this.search[domid].length) { this.search[domid] = phrase; this.display_continue(domid, 0); }
         }

        this.match = function(key, value)
        {
            if (!this.data) this.load();
            var results = [];
            for (var i in this.data)
            {
                if (this.data[i][key] == value) { results.push(this.data[i]); }
            }
            return results;
        }

        this.sethidden = function(key, value)
        {
            this.hidden[key] = value;
        }

        this.store = function(name, value)
        {
            name = this.me+'_'+name;
            var d = new Date;
            d.setTime(d.getTime() + 31536000000); // 24*60*60*1000*365;
            document.cookie = name + "=" + encodeURIComponent(JSON.stringify(value)) + ";path=/;expires=" + d.toGMTString();
        }

        this.storepush = function(name, value, max)
        {
            var old = this.retrieve(name);
            if (!old) old = new Array();
            old.push(value);
            this.store(name, old.splice(0,max));
        }

        this.retrieve = function(name)
        {
            name = this.me+'_'+name;
            var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
            return v ? JSON.parse(decodeURIComponent(v[2])) : null;
        }

        this.readmore = function(string, link, length)
        {
            if (!length) length = 150;
            if (!string || string == null) return '';
            if (string.length <= length) return string;
            full = strip_tags(string, '<p>');
            string = full.substring(0,length);
            var end = string.lastIndexOf(' ');
            if (end) string = string.substring(0,end);
           return string+'... <a href="'+link+'" title="'+escapeHtml(strip_tags(full.replace('<p>',"\n")))+'">Lire plus</a>';
        }

        this.shorttext = function(id, field, length)
        {
            var span = this.me+'-'+field+'-'+id
            return '<span id="'+span+'">'+this.lesstext(id, field, (length?length:100))+'</span>';
        }

        this.formattext = function(text)
        {
            return linkify(text);
        }

        this.lesstext = function(id, field, length)
        {
            var span = this.me+'-'+field+'-'+id;
            var string = this.formattext(this.getdata(id)[field]);
            var stringlength = strip_tags(string).length;
            if (!string || string == null) return '';
            if (stringlength <= length) return string;
            string = string.substring(0,length);
            var end = string.lastIndexOf(' ');
            if (end) string = string.substring(0,end);
            return string+'... <a onClick="javascript:$(\'#'+span+'\').html('+this.me+'.moretext('+id+',\''+field+'\', '+length+'));">Lire plus</a>';
        }

        this.moretext = function(id, field, length)
        {
            var span = this.me+'-'+field+'-'+id;
            var string = this.formattext(this.getdata(id)[field]);
            return string+' ... <a onClick="javascript:$(\'#'+span+'\').html('+this.me+'.lesstext('+id+',\''+field+'\', '+length+'));"> Close</a>';
        }


        this.taglist = function(tags, searchbox, size)
        {
            return tags?'<button type="button" class="btn '+(size?size:'btn-primary btn-xs')+'">'+tags.split(',').join('</button> <button type="button" class="btn '+(size?size:'btn-primary btn-xs')+'">')+'</button>':'';
        }

        this.list = function(domid,items, options)
        {
            var nodeid = domid+'List';
            var node = nodeid.substring(1);
            var childclass = domid.substring(1)+'Item';
            if (options['wrapper'] == 'ul') { var wrapper = 'ul'; var wrapper_class = (options['wrapper_class']?options['wrapper_class']:'list-group'); var childwrapper = 'li'; var childwrapper_class = (options['wrapper_class']?'':'list-group-item'); }
            else if (options['wrapper'] == 'panel') { var wrapper = 'div'; var wrapper_class = null; var childwrapper = 'div'; var childwrapper_class = 'panel panel-primary'; }
            else { var wrapper = (options['wrapper']?options['wrapper']:'div'); var wrapper_class = (options['wrapper_class']?options['wrapper_class']:null); var childwrapper = (options['childwrapper']?options['childwrapper']:'div'); var childwrapper_class = (options['childwrapper_class']?options['childwrapper_class']:null); }
            var isotope = options['isotope']?true:false;
            var nextpage = false;
            if (options['start'] == 0)
            {
                if (isotope && $(nodeid).data('isotope')) $(nodeid).isotope('remove', $(nodeid).isotope('getItemElements'));
                $(domid).empty();
                var tmp = $('<'+wrapper+(wrapper_class?' class="'+wrapper_class+'"':'')+' id="'+node+'"></'+wrapper+'>').appendTo(domid);
            }
            else
            {
                $tmp = $(nodeid+'Infinite'); 
                if (isotope && $(nodeid).data('isotope')) $(nodeid).isotope('remove', $tmp).isotope('layout');
                $tmp.unbind('inview'); $tmp.remove();
            }
            for (var i=0; i<items.length; i++)
            {
                var child = items[i];
                if (!options['raw'])
                    var html = '<'+childwrapper+attr('class', [childclass, child['class'], childwrapper_class], child.isnew?'new':null)+attr('search', child.search)+'>'+child.html+'</'+childwrapper+'>'+
                        (child.infinitescroll?'<'+childwrapper+attr('class', [childclass, child['class'], childwrapper_class])+attr('id', node+'Infinite')+'>Loading...'+'</'+childwrapper+'>':'');
                else var html = child.html;
                if (child.footer) html += child.footer;
                if (isotope && $(nodeid).data('isotope')) { var $tmp = $(html); $(nodeid).append($tmp).isotope( 'appended', $tmp ); }
                else $(nodeid).append(html);
                if (child.infinitescroll) nextpage = true;
            }
            if (options['start'] == 0)
            {
                if (options['header']) $(domid).prepend(options['header']);
                if (options['footer']) $(domid).append(options['footer']);
                if (isotope) $(nodeid).isotope({ itemSelector: '.'+childclass, layoutMode: 'fitRows' });
            }
//            else $(nodeid).isotope();

            if (nextpage) $(nodeid+'Infinite').one('inview', function() { self.display_continue(domid, options['offset']); } );
        }

        this.text = function(domid, text)
        {
            $(domid).html(text);
        }

        this.setindex = function()
        {
            if (!this.data_index)
            {
                this.data_index = {};
                for (var i=0; i< this.data.length; i++) this.data_index[this.data[i]['id']] = i;
            }
        }

        this.getdata = function(id)
        {
            this.setindex();
            if (this.data_index[id] != null) return this.data[this.data_index[id]];
            return null;
        }

        this.renderdays = function(date)
        {
            var days = { '0': 'today', '-1': 'yesterday', '1': 'tomorrow' };
            var daysDiff = moment(date).startOf('day').diff(moment().startOf('day'), 'days');
            if (Math.abs(daysDiff) <= 1)  return days[daysDiff];
            return moment().add(daysDiff, 'days').fromNow();;
        }

        this.renderformfield = function(field)
        {
            if (!field['value']) field['value'] = field['default']?field['default']:'';
            if (field['type'] == 'input') return '<input class="form-control border no-shadow no-rounded" placeholder="'+(field['title']?field['title']:'')+'" name="'+field['field']+'" value="'+field['value']+'">'+(field['submit']?'<span class="input-group-btn"> <button class="btn btn-success no-rounded" type="button">Send</button>':'');
            if (field['type'] == 'date') return (field['title']?field['title']+' : ':'')+'<div class="datepicker"><input type="hidden" name="'+field['field']+'" value="'+field['value']+'"></div>';
            else if (field['type'] == 'textarea') return '<textarea class="form-control border no-shadow no-rounded" placeholder="'+(field['title']?field['title']:'')+'" name="'+field['field']+'">'+field['value']+'</textarea>';
            else if (field['type'] == 'select' || field['type'] == 'select2')
            {
                console.log(field['options']);
                if (field['options'].length < 1)
                {
                    var html = "Pas d'options";
                }
                else
                {
                    var html = (field['title']?field['title']+' : ':'')+'<select class="'+(field['type'] == 'select2'?'select2 ':'')+'form-control" name="'+field['field']+'"><option value=""></option>';
                    for (var option in field['options']) { html += '<option value="'+option+'"'+(field['value']==option?' selected':'')+'>'+field['options'][option]+'</option>'; }
                    html += '</select>';
                }
                return html;
            }
            else if (field['type'] == 'boolean') { return '<label class="label-checkbox"><input type="checkbox" name="'+field['field']+'" value="true"'+(field['value']!='' && field['value']!='false'?' checked':'')+'><span class="custom-checkbox"></span>'+(field['title']?' '+field['title']:'')+'</label>'; }
            else if (field['type'] == 'radio')
            {
                if (field['value']) { field['options'] = {}; field['options'][field['value']] = field['title']; }
                if (field['options'])
                {
                    var html = '';
                    for (var option in field['options']) html += '<label class="label-checkbox"><input type="radio" name="'+field['field']+'" value="'+option+'"'+(option==field['selected']?' checked':'')+'><span class="custom-radio"></span>'+field['options'][option]+'</label>';
                    return html;
                }
//                else return '<label class="label-checkbox"><input type="radio" name="'+field['field']+'" value="'+field['value']+'"'+(field['value']==field['selected']?' checked':'')+'><span class="custom-radio"></span>'+(field['title']?' '+field['title']:'')+'</label>';
            }
        }

        this.renderformset = function(formset)
        {
            var output = '';
            for (var i=0; i<formset['elements'].length; i++)
            {
                var row = formset['elements'][i], columns = 12;
                output += '<div class="form-group">';
                if (Array.isArray(row))
                {
                    for (var j=0; j<row.length; j++)
                    {
                        var result = this.renderformset({ elements: row[j], data: formset['data'] });
                        var cols = (row[j][0]['width']?row[j][0]['width']:parseInt(columns/(row.length-j)));
                        columns = columns - cols;
                        output += '<div class="mx-auto col-md-'+cols+'">'+result['html']+'</div>';
                        if (result['date']) formset['date'] = true;
                    }
                }
                else
                {
                    if (formset['data'] && formset['data'][row['field']])
                    {
                        if (row['type'] == 'radio') row['selected'] = formset['data'][row['field']]; else row['value'] = formset['data'][row['field']];
                        if (row['type'] == 'select' || row['type'] == 'select2' ) row['id'] = formset['data'][row['field']+'_id'];
                    }
                    output += this.renderformfield(row);
                    if (row['submit']) formset['submit-button'] = true; 

                    if (row['type'] == 'date') formset['date'] = true;
                }
                output += '</div>';
            }
            formset['html'] = output;
            return formset;
        }

        this.renderform = function(domid, elements, options)
        {
            var i, found, data = (options['hidden'] && options['hidden']['id']?this.getdata(options['hidden']['id']):false);
            if (data && options['subobject'] && options['hidden'][options['subobject']+'__id'] && data[options['subobject']]) // Subobject fields get translated to subobject__field
            {
                found = false;
                var search = data[options['subobject']];
                for (i=0; i<search.length; i++)
                {

                    if (search[i]['id'] == options['hidden'][options['subobject']+'__id'])
                    {
                        data = {};
                        for (var prop in search[i]) data[options['subobject']+'__'+prop] = search[i][prop];
                    }
                }
            }
            if (options['hidden'] && options['hidden']['id'] && data == null) return "Ca n'existe plus, desole"; //
            if (options['default']) { if (!data) data = {};for (i in options['default']) { if (!data[i]) data[i] = options['default'][i]; } }
            var id = (domid.substring(0,1)=='#'?'id':'class')+'="'+domid.substring(1)+'form"';
            var success = (options['submit']?'if ('+this.me+'.update(\''+domid+'form\')) '+options['submit']:this.me+'.update(\''+domid+'form\')');
            var html = '<form class="form-horizontal" '+id+' onSubmit="'+success+'; return false;">'+(options['header']?options['header']:'')+(options['bodytop']?options['bodytop']:'')+(!options['delete']?'<input type="hidden" name="edit" value="'+(options['form']?options['form']:'form')+'">':'');
            var result = this.renderformset({ elements: elements, data: data, date: false });
            if (data && this.passthru) for (var passfield in this.passthru) options['hidden'][this.passthru[passfield]] = data[this.passthru[passfield]];
            if (this.hidden) { if (!options['hidden']) options['hidden'] = {}; for (var field in this.hidden) { if (!options['hidden'][field]) options['hidden'][field] = this.hidden[field]; } }
            for (var option in options['hidden']) html+= '<input type="hidden" name="'+option+'" value="'+options['hidden'][option]+'">';
            html += result['html'];
            html += (options['submit-button']&&!result['submit-button']?options['submit-button']:'')+'<div id="'+domid.substring(1)+'form_results" class="modalresults"></div>'+'<div id="'+domid.substring(1)+'form_errors" class="modalerrors"></div>'+(options['footer']?options['footer']:'')+'</form>';
            return html;
        }

        this.formtypes = function(row, types)
        {
            if (!types) types = [];
            for (var i=0; i<row.length; i++)
            {
                if (Array.isArray(row[i])) types = types.concat(this.formtypes(row[i]));
                else types.push(row[i]['type']); 
            }
            return types;
        }

        this.forminitialise = function(domid, modal, form)
        {
            var select2options = modal? { dropdownParent: $(domid), width: "100%" } : { width: "100%" } ;
            var types = this.formtypes(form, false);
            if (types.includes('select2')) $(".select2").select2(select2options);
            if (types.includes('date')) $('.datepicker').datepicker({ todayBtn: 'linked', todayHighlight: true, format: 'yyyy-mm-dd', });
        }

        this.clickaction = function(options)
        {

        }

        this.fullname = function(a)
        {
            if (!a) return "noname";
            if (a['forename'] && a['surname']) return a['forename']+' '+a['surname'];
            if (a['forename']) return a['forename']; if (a['surname']) return a['surname'];
            return "missingname";
        }

        this.options = function(field)
        {
            if (!this.data) this.syncload();
            var options = {};
            console.log(this.data);
            for (var i=0; i<this.data.length; i++) options[this.data[i]['id']] = (field=='fullname'?this.fullname(this.data[i]):this.data[i][field]);
            return options;
        }

        this.edit = function(domid, options)
        {
            var form = (options['form']?this[options['form']]():this.form())
            options['submit-button'] = '<div class="row"><div class="col-md-12" align="center"><button type="submit" class="btn btn-sm btn-success"><i class="fa fa-edit fa-lg"></i> Enregistrer</button></div></div>';
            $(domid).html(this.renderform(domid, form, options));
            this.forminitialise(domid, false, form);
        }

        this.modal = function(domid, options)
        {
            if (!options) options = {};
            options['header'] = '<div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Fermer"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">'+(options['title']?options['title']:'Missing title')+'</h4></div><div class="modal-body">';
            options['footer'] = '</div><div class="modal-footer">'+(!options['delete'] && options.hidden && options.hidden.id?'<button onClick="javascript:'+this.me+".modal_delete('"+domid+"', "+options.hidden.id+(options['subobject']?",'"+options['subobject']+"',"+options.hidden[options['subobject']+'__id']:'')+'); return false;" class="pull-left btn btn-danger">Supprimer</button>':'')+'<button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button> <button type="submit" class="btn btn-primary">Sauver</button></div>';
            options['submit'] = "$('"+domid+"').modal('hide');";
            var modal = $(domid), form = (options['form']?this[options['form']]():this.form());
            modal.find('.modal-content').html(this.renderform(domid, form, options));
            this.forminitialise(domid, true, form);
            modal.modal('show');
        }

        this.confirm_delete = function()
        {
            if (this.trash)
            {
                var options = [];
                for (var i in this.trash) options.push({ type: 'radio', field: 'trash', value: this.trash[i], title: this.trash[i], });
                options.push({ type: 'radio', field: 'trash', value: 'confirm', title: 'Supprimer completement', });
                return options;
            }
            return [
                        { type: 'boolean', field: 'confirm', value: false, title: 'cochez pour confirmer la suppression', },
                    ];
        }


        this.modal_delete = function(domid, id, subobject, subobject_id)
        {
            var options = { title: 'Supprimer', form : 'confirm_delete', hidden : { id : id, 'delete': true, 'subobject' : (subobject?subobject:false) }, 'default': false, 'delete': true };
            options['hidden'][subobject+'__id'] = subobject_id;
            this.modal(domid,options);
        }

}
