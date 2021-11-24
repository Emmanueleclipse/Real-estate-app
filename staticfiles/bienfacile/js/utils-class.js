
/* Layout functions */
function panelTop(title, actions = false)
{
    var html = '<div class="panel-heading">'+title;
    if (actions)
    {
        html += '<div class="btn-group pull-right"><button class="btn btn-primary btn-xs dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="caret"></span><span class="sr-only">Toggle Dropdown</span></button><ul class="dropdown-menu">';
        for (var i in actions) if (i == '') html += '<li><hr/></li>'; else html += '<li><a href="'+actions[i]+'">'+i+'</a></li>';
        html += '</ul></div>';
    }
    html += '</div>';
    return html;
}
function panelBody(html) { return '<div class="panel-body">'+html+'</div>'; }
function divRow(html) { return '<div class="row">'+html+'</div>';}
function divCol(html, num=12) { return '<div class="mx-auto col-md-'+num+'">'+html+'</div>'; }
function addNewButton(title,action) { return '<button class="btn btn-xs btn-default" type="button"><i class="fa fa-plus"></i> '+title+'</button>'; }

function modifyButton(title, actions, replace = {})
{
    var html = '<div class="btn-group pull-right"><button class="btn btn-default dropdown-toggle" data-toggle="dropdown">Action <span class="caret"></span></button><ul class="dropdown-menu">';
    for (var i in actions)
        html += '<li><a href="'+actions[i]+'">'+i+'</a></li>';
    html += '</ul></div>';
    
    for (var i in replace) { html = replaceAll(html,i, replace[i]); }
    return html;
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

function textlength(string, length) {
    if (string.length <= length) return string;
    string = string.substring(0,length);
    end = string.lastIndexOf(' ');
    if (end) string = string.substring(0,end);
    return string+'...';
}

function numberWithCommas(x) { if (x) return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); return x; }
function capitalise(phrase) { return phrase.charAt(0).toUpperCase() + phrase.substring(1); }

function extractkeywords(phrase)
{
    if (!phrase || phrase.length==0) return false;
    if (phrase.indexOf(' ')>0) return phrase.split(' ');
    return [ phrase ];
}

function searchstring(search,keywords)
{
    var ignore = ['m', 'mme', 'mr', 'mlle', 'mm'];
    pos = 0;
    for(var i = 0 , len = keywords.length; i < len; i++){
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


/* FeedObject for taking and displaying JSON feeds */

function hashCode(target){
    var hash = 0;
    if (target.length == 0) return hash;
    for (i = 0; i < target.length; i++)
    {
        char = target.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
}

/* Simple JavaScript Inheritance
 * By John Resig https://johnresig.com/
 * MIT Licensed.
 */
// Inspired by base2 and Prototype
(function(){
  var initializing = false, fnTest = /xyz/.test(function(){xyz;}) ? /\b_super\b/ : /.*/;
 
  // The base Class implementation (does nothing)
  this.Class = function(){};
   
  // Create a new Class that inherits from this class
  Class.extend = function(prop) {
    var _super = this.prototype;
     
    // Instantiate a base class (but only create the instance,
    // don't run the init constructor)
    initializing = true;
    var prototype = new this();
    initializing = false;
     
    // Copy the properties over onto the new prototype
    for (var name in prop) {
      // Check if we're overwriting an existing function
      prototype[name] = typeof prop[name] == "function" && 
        typeof _super[name] == "function" && fnTest.test(prop[name]) ?
        (function(name, fn){
          return function() {
            var tmp = this._super;
             
            // Add a new ._super() method that is the same method
            // but on the super-class
            this._super = _super[name];
             
            // The method only need to be bound temporarily, so we
            // remove it when we're done executing
            var ret = fn.apply(this, arguments);        
            this._super = tmp;
             
            return ret;
          };
        })(name, prop[name]) :
        prop[name];
    }
     
    // The dummy class constructor
    function Class() {
      // All construction is actually done in the init method
      if ( !initializing && this.init )
        this.init.apply(this, arguments);
    }
     
    // Populate our constructed prototype object
    Class.prototype = prototype;
     
    // Enforce the constructor to be what we expect
    Class.prototype.constructor = Class;
 
    // And make this class extendable
    Class.extend = arguments.callee;
     
    return Class;
  };
})();


var FeedObject = function(feedurl) {

            this.url = feedurl;
            this.data = false;
            this.new = [];
            this.data_index = false;
            this.pager = false;
            this.perpage = 5;
            this.callbackrender = {};
            this.search = {};
            var self=this;
        };

$.extend(FeedObject.prototype, {
        refresh: function(timeout) {
            setInterval(function(){ this.load(); }, timeout*1000);
        },

        updatedata: function(a) {
            var hash = hashCode(JSON.stringify(a));
            if (this.data && this.hash == hash) return false;
            if (this.data)
            {
                this.setindex();
                for (var i=0; i < a.length; i++)
                {
                    if (this.data_index[a[i].id] == null) this.new.push(a[i].id);
                }
            }
            this.data_index = false;
            this.data = a;
            this.hash = hash;
            for (var i in this.new) this.data[i].new = true;
            this.total = this.data.length;
            return true;
        },

        load: function(display = true) {
//            jQuery.ajax({ url: this.url, cache: false, crossDomain: true, async: false, dataType: 'jsonp', jsonp: "callback", context: this,
            jQuery.ajax({ url: this.url, cache: false, crossDomain: false, async: true, dataType: 'json', context: this,

                success: function(a){
                    if (this.updatedata(a) && display) this.display();
               },
                error: function(xhr, textStatus, errorThrown){
                     alert(textStatus+': '+xhr.responseText['error']); }
            });
        },

        update: function(formid, data2 = null, data3 = null, data4 = null) {
            var data1 = {};
            var tmp = $(formid).serializeArray();
            for (i=0; i<tmp.length; i++) data1[tmp[i]['name']]=tmp[i]['value'];
             data = Object.assign({},data1, data2, data3, data4);
            document.getElementById(formid.substring(1)).reset();
//            jQuery.ajax({ url: this.url, cache: false, crossDomain: true, async: false, dataType: 'jsonp', jsonp: "callback", context: this,
            jQuery.ajax({ url: this.url, cache: false, crossDomain: false, async: true, dataType: 'json', method: 'POST', data: data, context: this,

                success: function(a){
                    this.updatedata(a);
                    this.display();
               },
                error: function(xhr, textStatus, errorThrown){
                     alert(textStatus+': '+JSON.parse(xhr.responseText)['error']); }
            });
        },

        attach: function(domid, func, options) { this.callbackrender[domid] = [func, options]; },

        display: function() {
            if (!this.data) { this.load(); return; }
            for (domid in this.callbackrender)
            {
                this.continue(domid, 0);
            }
        },

        continue: function(domid, offset=0)
        {
            func = this.callbackrender[domid][0];
            opts = this.callbackrender[domid][1];
            opts['start'] = offset;
            opts['infiniteid'] = domid+'scroll';
            opts['listid'] = domid+'List';
            opts['list-element'] = opts['listid'].substring(1);
            var perpage = opts['perpage']?opts['perpage']:this.perpage;
            var finish = opts['max']&&opts['max']<this.total?opts['max']:this.total;
            var shown = 0;
            var items = [];
            while (offset < finish && shown < perpage)
            {
                var item = this.data[offset];
                var filter = false;
                if (opts['filter'])
                {
                    for (var key in opts['filter']) { if (item[key] != opts['filter'][key]) filter = true; }
                }
                if (!filter)
                {
                    shown+=1;
                    item.infinitescroll = (shown == perpage?true:false);
                    items.push(item);
                }
                offset+=1;
            }
            opts['offset'] = offset; opts['shown'] = shown;
            this[func](domid, items, opts);
        },


        filteron: function(domid, phrase) {
            if (!this.search['domid'] || phrase.length > this.search['domid'].length)
            {
                var elems = $(domid).isotope('getItemElements');
                var numelems = elems.length;
                var filterkeywords = extractkeywords(phrase);
                if (!filterkeywords  || numelems == 0) return;

                for (j=0; j<numelems; j++)
                {
                    if (!searchstring(elems[j].getAttribute('search'),filterkeywords)) $(elems[j]).hide();
                }
                $(domid).isotope('layout');
                

            }
            else if (phrase.length < this.search[domid].length) this.continue(domid, 0);
            this.search[domid] = phrase;
        },

        shorttext: function(id, field, length = 160)
        {
            span = this.me+'-'+field+'-'+id
            return '<span id="'+span+'">'+this.lesstext(id, field, length)+'</span>';
        },

        lesstext: function(id, field, length)
        {
            span = this.me+'-'+field+'-'+id;
            string = this.getdata(id)[field];
            if (string.length <= length) return string;
            string = string.substring(0,length);
            end = string.lastIndexOf(' ');
            if (end) string = string.substring(0,end);
            return string+'... <a onClick="javascript:$(\'#'+span+'\').html('+this.me+'.moretext('+id+',\''+field+'\', '+length+'));">Lire plus</a>';
        },

        moretext: function(id, field, length)
        {
            span = this.me+'-'+field+'-'+id;
            string = this.getdata(id)[field];
            return string+' <a onClick="javascript:$(\'#'+span+'\').html('+this.me+'.lesstext('+id+',\''+field+'\', '+length+'));">Close</a>';
        },


        taglist: function(tags, searchbox = false, size = false)
        {
            return tags?'<button type="button" class="btn '+(size?size:'btn-primary btn-xs')+'">'+tags.split(',').join('</button> <button type="button" class="btn '+(size?size:'btn-primary btn-xs')+'">')+'</button>':'';
        },

        list: function(domid,items, options)
        {
            var nodeid = domid+'List';
            var node = nodeid.substring(1);
            var childclass = domid.substring(1)+'Item';
            if (options['wrapper'] == 'ul') { var wrapper = 'ul'; var wrapper_class = (options['wrapper_class']?options['wrapper_class']:'list-group'); var childwrapper = 'li'; var childwrapper_class = (options['wrapper_class']?'':'list-group-item'); }
            else if (options['wrapper'] == 'panel') { var wrapper = 'div'; var wrapper_class = null; var childwrapper = 'div'; var childwrapper_class = 'panel panel-primary'; }
            else { var wrapper = (options['wrapper']?options['wrapper']:'div'); var wrapper_class = null; var childwrapper = (options['wrapper']?options['wrapper']:'div'); var childwrapper_class = null; }
            var isotope = options['isotope']?true:false;
            var nextpage = false;
            if (options['start'] == 0)
            {
                if (isotope) $(nodeid).isotope('remove', $(nodeid).isotope('getItemElements'));
                $(domid).empty();
                tmp = $('<'+wrapper+(wrapper_class?' class="'+wrapper_class+'"':'')+' id="'+node+'"></'+wrapper+'>').appendTo(domid);
            }
            else
            {
                $(nodeid+'Infinite').unbind('inview');
                $(nodeid+'Infinite').remove();
            }
            for (var i=0; i<items.length; i++)
            {
                child = items[i];
                html = '<'+childwrapper+attr('class', [childclass, child.class, childwrapper_class], child.new?'new':null)+attr('search', child.search)+child.html+'</'+childwrapper+'>'+
                        (child.infinitescroll?'<div id='+node+'Infinite'+'>Loading...</div>':'');
                $tmp = $(nodeid).append(html);
                if (isotope) $tmp.isotope( 'insert', html ).isotope('layout');
                if (child.infinitescroll) nextpage = true;
            }
            if (options['start'] == 0)
            {
                if (options['header']) $(domid).prepend(options['header']);
                if (options['footer']) $(domid).append(options['footer']);
            }

            if (nextpage) $(nodeid+'Infinite').one('inview', function() { this.continue(domid, options['offset']); } );
            if (isotope) $(domid).isotope({ itemSelector: '.'+childclass, layoutMode: 'fitRows' });


        },

        setindex: function()
        {
            if (!this.data_index)
            {
                this.data_index = {};
                for (var i=0; i< this.data.length; i++) this.data_index[this.data[i]['id']] = i;
            }
        },

        getdata: function(id)
        {
            this.setindex();
            if (this.data_index[id] != null) return this.data[this.data_index[id]];
            return null;
        },

        renderdays: function(date)
        {
            days = { '0': 'today', '-1': 'yesterday', '1': 'tomorrow' };
            daysDiff = moment(date).startOf('day').diff(moment().startOf('day'), 'days');
            if (Math.abs(daysDiff) <= 1)  return days[daysDiff];
            return moment().add(daysDiff, 'days').fromNow();;
        },

        renderformfield: function(field)
        {
            if (field['type'] == 'input') return '<input class="form-control border no-shadow no-rounded" placeholder="'+(field['title']?field['title']:'')+'" name="'+field['field']+'" value="'+(field['value']?field['value']:'')+'">'+(field['submit']?'<span class="input-group-btn"> <button class="btn btn-success no-rounded" type="button">Send</button>':'');
            if (field['type'] == 'date') return (field['title']?field['title']+' : ':'')+'<div class="datepicker"><input type="hidden" name="'+field['field']+'" value="'+(field['value']?field['value']:'')+'"></div>';
            else if (field['type'] == 'textarea') return '<textarea class="form-control border no-shadow no-rounded" placeholder="'+(field['title']?field['title']:'')+'" name="'+field['field']+'">'+(field['value']?field['value']:'')+'</textarea>';
            else if (field['type'] == 'select')
            {
                var html = (field['title']?field['title']+' : ':'')+'<select class="form-control" name="'+field['field']+'"><option value=""></option>';
                for (option in field['options']) { html += '<option value="'+option+'"'+(field['value']==option?' selected':'')+'>'+field['options'][option]+'</option>'; }
                html += '</select>';
                return html;
            }
            else if (field['type'] == 'boolean') return '<label class="label-checkbox"><input type="checkbox" name="'+field['field']+'" value="true"'+(field['value']?' checked':'')+'><span class="custom-checkbox"></span>'+(field['title']?' '+field['title']:'')+'</label>';
        },

        renderformset: function(formset)
        {
            var output = '';
            for (var i=0; i<formset['elements'].length; i++)
            {
                var row = formset['elements'][i];
                output += '<div class="form-group">';
                if (Array.isArray(row))
                {
                    for (var j=0; j<row.length; j++)
                    {
                        var result = this.renderformset({ elements: row[j], data: formset['data'] });
                        output += '<div class="mx-auto col-md-'+(12/row.length)+'">'+result['html']+'</div>';
                        if (result['date']) formset['date'] = true;
                    }
                }
                else
                {
                    if (formset['data'] && formset['data'][row['field']]) { row['value'] = formset['data'][row['field']]; }
                    output += this.renderformfield(row);
                    if (row['submit']) formset['submit-button'] = true; 

                    if (row['type'] == 'date') formset['date'] = true;
                }
                output += '</div>';
            }
            formset['html'] = output;
            return formset;
        },

        renderform: function(domid, elements, options)
        {
            var data = (options['hidden'] && options['hidden']['id']?this.getdata(options['hidden']['id']):false);
            var id = (domid.substring(0,1)=='#'?'id':'class')+'="'+domid.substring(1)+'form"';
            var html = '<form class="form-horizontal" '+id+' onSubmit="'+this.me+'.update(\''+domid+'form\');'+(options['submit']?options['submit']:'')+' return false;">'+(options['header']?options['header']:'')+(!options.delete?'<input type="hidden" name="edit" value=true>':'');
            var result = this.renderformset({ elements: elements, data: data, date: false });
            if (data && this.passthru) for (var passfield in this.passthru) options['hidden'][this.passthru[passfield]] = data[this.passthru[passfield]];
            if (this.hidden) { if (!options['hidden']) options['hidden'] = {}; for (var field in this.hidden) { if (!options['hidden'][field]) options['hidden'][field] = this.hidden[field]; } }
            for (var option in options['hidden']) html+= '<input type="hidden" name="'+option+'" value="'+options['hidden'][option]+'">';
            html += result['html'];
            html += (options['submit-button']&&!result['submit-button']?options['submit-button']:'')+(options['footer']?options['footer']:'')+'</form>'+(result['date']?"<script>$('.datepicker').datepicker({ todayBtn: 'linked', todayHighlight: true, format: 'yyyy-mm-dd', });</script>":'');
            return html;
        },

        clickaction: function(options)
        {

        },

        edit: function(domid, options)
        {
            options['submit-button'] = '<div class="row"><div class="col-md-12" align="center"><button type="submit" class="btn btn-sm btn-success"><i class="fa fa-edit fa-lg"></i> Enregistrer</button></div></div>';
            $(domid).html(this.renderform(domid,this.form(), options));
        },

        modal: function(domid, options = {})
        {
            options['header'] = '<div class="modal-body"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Fermer"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">'+(options['title']?options['title']:'Missing title')+'</h4></div><p>';
            options['footer'] = '</div><div class="modal-footer">'+(!options.delete && options.hidden && options.hidden.id?'<button onClick="javascript:'+this.me+".modal_delete('"+domid+"', "+options.hidden.id+'); return false;" class="pull-left btn btn-danger">Supprimer</button>':'')+'<button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button> <button type="submit" class="btn btn-primary">Sauver</button></div>';
            options['submit'] = "$('"+domid+"').modal('hide');";
            modal = $(domid);
            modal.find('.modal-content').html(this.renderform(domid,(options['form']?this[options['form']]():this.form()), options));
            modal.modal('show');
        },

        confirm_delete: function()
        {
            return [
                        { type: 'boolean', field: 'confirm', title: 'cochez pour confirmer la suppression', },
                    ];
        },

        modal_delete: function(domid, id)
        {
            options = { title: 'Supprimer', form : 'confirm_delete', hidden : { id : id, delete: true }, delete: true };
            this.modal(domid,options);
        },

    }
);
