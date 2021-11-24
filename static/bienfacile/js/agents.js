
function numberWithCommas(x) { return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }

function extractkeywords(phrase)
{
    if (!phrase || phrase.length==0) return false;
    if (phrase.indexOf(' ')>0) return phrase.split(' ');
    return [ phrase ];
}

function searchstring(search,keywords)
{
    pos = 0;
    for(var i = 0 , len = keywords.length; i < len; i++){
        if (keywords[i] == '') continue;
        found = search.indexOf(keywords[i]);
        if (found == -1) return false;
        else if (found < pos) return false;
        else pos = found;
    }
    return true;
}

(function($){
 
    AgentFeedObject = function(el, options) {
        this.agents = {};
        this.create(el, options);
        this.loading = false;
    };
 
    $.extend(AgentFeedObject.prototype, {
 
         display: function(offset) {
            if (this.loading == true) { return; }
            this.loading = true;
            if (offset == 0)
            {
                $('#agents').isotope('remove', $('#agents').isotope('getItemElements'));
                $('#agents').empty();
            }
            else
            {
                $('#infinitescroll').unbind('inview');
                $('#infinitescroll').removeAttr('id');
            }
            total = this.agents.length;
            shown = 0; perpage = 20;
            keywords = extractkeywords(this.search);

            while (offset < total && shown < perpage)
            {
                var item = this.agents[offset];
                if (!keywords || searchstring(item.search,keywords))
                {
                    shown += 1;
                    if (item.mobile) var mobile = 'Téléphone: '+item.mobile+'<br/><br/>'; else var mobile = '';
                    if (item.email) var email = '<a href="mailto:'+item.email+'"><i class="fa fa-envelope"></i></a> '; else var email = '';
//                     if (item.image != '')
//                        var image = '<img width="300" height="225" src="'+item.image+'" alt="" />';
//                    else var image = '<div style="width:200px;height:150px;overflow:none;">'+item.title+'</div>';
                    if (shown == perpage) { var infinitescroll = ' id="infinitescroll"';  } else var infinitescroll = '';
                    var $html = $('<div class="agent"'+infinitescroll+' style="color:#000" search="'+item.search+'"><h4>'+item.forename+' '+item.surname+'</h4>'+mobile+email+'<a href="/agence#'+item.agencyid+'">'+item.agency+'</a></div>');
                    $('#agents').append( $html ).isotope( 'insert', $html ).isotope('layout');
                }
                offset+=1;
            }
            $('#infinitescroll').one('inview', function() { feed.display(offset); } );
            this.loading = false;
        },



        filteron: function(phrase) {
//            if (this.loading == true) { return; }
            if (phrase.length > this.search.length)
            {
                total = this.agents.length;
                var elems = $('#agents').isotope('getItemElements');
                var numelems = elems.length;
                var filterkeywords = extractkeywords(phrase);
                if (filterkeywords) 
                {
                    for (j=0; j<numelems; j++)
                    {
                        if (!searchstring(elems[j].getAttribute('search'),filterkeywords)) $(elems[j]).hide();
                    }
                }
                $('#agents').isotope('layout');
                this.search = phrase;

            }
            else if (phrase.length < this.search.length) { this.search = phrase; this.display(0); }
        },
 

        setproperty: function(key, value) {
            this[key] = value;
            $.cookie(key, value, { path: '/' });
        },
 
        create: function(el, options) {
            this.search = '';
            var url = '/json_agents/';
            // jQuery AJAX call
            $('#agents').loading({ message: 'Loading...' });
//            jQuery.ajax({ url: url, cache: false, crossDomain: true, async: false, dataType: 'jsonp', jsonp: "callback", context: this,
            jQuery.ajax({ url: url, cache: false, crossDomain: false, async: true, dataType: 'json', context: this,

                success: function(a){
                    this.agents = a;
                    $('#agents').loading('stop');
                    this.display(0);
               },
                error: function(xhr, textStatus, errorThrown){
                     alert(textStatus+': '+errorThrown); }
            });
        }
    });
 
    $.fn.agentFeed = function(options, callback){
        var d = {};
        this.each(function(){
            var s = $(this);
            d = s.data("agentfeed");
            if (!d){
                d = new AgentFeedObject(this, options, callback);
                s.data("agentfeed", d);
            }
        });
        return d;
    };

})(jQuery);
