
function numberWithCommas(x) { return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }

function short_address(address) { return address.replace('Boulevard', 'Bvd').replace('Avenue', 'Av.').replace(', ', ' '); }

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
 
    AgencyFeedObject = function(el, options) {
        this.agencies = {};
        this.create(el, options);
        this.loading = false;
    };
 
    $.extend(AgencyFeedObject.prototype, {
 
         display: function(offset) {
            if (this.loading == true) { return; }
           this.loading = true;
            if (offset == 0)
            {
                $('#agencies').isotope('remove', $('#agencies').isotope('getItemElements'));
                $('#agencies').empty();
            }
            else
            {
                $('#infinitescroll').unbind('inview');
                $('#infinitescroll').removeAttr('id');
            }
            total = this.agencies.length;
            shown = 0; perpage = 20;
            keywords = extractkeywords(this.search);

            while (offset < total && shown < perpage)
            {
                var item = this.agencies[offset];
                if (!keywords || searchstring(item.search,keywords))
                {
                    shown += 1;
                    var branch = '<h5>&nbsp;</h5>';
                    if (item.branch) branch = '<h5>('+item.branch+')</h5>';
//                     if (item.image != '')
//                        var image = '<img width="300" height="225" src="'+item.image+'" alt="" />';
//                    else var image = '<div style="width:200px;height:150px;overflow:none;">'+item.title+'</div>';
                    if (shown == perpage) { var infinitescroll = ' id="infinitescroll"';  } else var infinitescroll = '';
                    var $html = $('<div class="agency"'+infinitescroll+' style="color:#000" search="'+item.search+'"><h4>'+item.name+'</h4>'+branch+'Téléphone: '+item.telephone+'<br/><br/><a href="'+item.web+'"><i class="fa fa-globe fa-lg"></i></a> <a href="mailto:'+item.email+'"><i class="fa fa-envelope"></i></a> <a href="/agence#'+item.agencyid+'">'+short_address(item.address)+' '+item.postcode+' '+item.city+'</a></div>');
                    $('#agencies').append( $html ).isotope( 'insert', $html ).isotope('layout');
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
                total = this.agencies.length;
                var elems = $('#agencies').isotope('getItemElements');
                var numelems = elems.length;
                var filterkeywords = extractkeywords(phrase);
                if (filterkeywords) 
                {
                    for (j=0; j<numelems; j++)
                    {
                        if (!searchstring(elems[j].getAttribute('search'),filterkeywords)) $(elems[j]).hide();
                    }
                }
                $('#agencies').isotope('layout');
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
            var url = '/json_agences/';
            // jQuery AJAX call
            $('#agencies').loading({ message: 'Loading...' });
//            jQuery.ajax({ url: url, cache: false, crossDomain: true, async: false, dataType: 'jsonp', jsonp: "callback", context: this,
            jQuery.ajax({ url: url, cache: false, crossDomain: false, async: true, dataType: 'json', context: this,

                success: function(a){
                    this.agencies = a;
                    $('#agencies').loading('stop');
                    this.display(0);
               },
                error: function(xhr, textStatus, errorThrown){
                     alert(textStatus+': '+errorThrown); }
            });
        }
    });
 
    $.fn.agencyFeed = function(options, callback){
        var d = {};
        this.each(function(){
            var s = $(this);
            d = s.data("agencyfeed");
            if (!d){
                d = new AgencyFeedObject(this, options, callback);
                s.data("agencyfeed", d);
            }
        });
        return d;
    };

})(jQuery);
