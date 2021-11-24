
function numberWithCommas(x) { return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }

(function($){
 
    ClassifiedFeedObject = function(el, options) {
        this.annonces = {};
        this.create(el, options);
        this.loading = false;
    };
 
    $.extend(ClassifiedFeedObject.prototype, {
 
         display: function(offset) {
            if (this.loading == true) { return; }
            this.loading = true;
            if (offset == 0)
            {
                $('#classifieds').isotope('remove', $('#classifieds').isotope('getItemElements')); // you can remove multiple items with jQuery and also append new itmes
                $('#classifieds').empty();
            }
            else
            {
                $('#infinitescroll').unbind('inview');
                $('#infinitescroll').removeAttr('id');
            }
            total = this.annonces.length;
            shown = 0; perpage = 20;
            while (offset < total && shown < perpage)
            {
                var item = this.annonces[offset];
                if (   (this.maxprice >= 500000 || item.price <= this.maxprice)
                    && (this.maxpricepersqm >= 10000 || item.pricepersqm <= this.maxpricepersqm)
                    && (this.locations.length == 0 || this.locations.indexOf(item.menugroup) != -1)
                    && (this.sortby != 'pricedrop' || item.pricedrop > 0) && (this.sortby != 'pricepersqm' || item.pricepersqm > 0))
                {
                    shown += 1;
                    var ribbon = '';
                    var location = item.location;
                    if (location.length > 16) location = "<span style=\"font-size: 72%\">"+location+"</span>";
                    if (item.image != '')
                        var image = '<img width="300" height="225" src="'+item.image+'" alt="" />';
                    else var image = '<div style="width:300px;height:225px;overflow:none;">'+item.title+'</div>';
                    if (shown == perpage) { var infinitescroll = ' id="infinitescroll"';  } else var infinitescroll = '';
                    if (item.pricedrop > 0) ribbon += '<div class="ribbon-wrapper"><div class="ribbon-inner shadow-pulse bg-warning">'+item.pricedrop+'% Off</div></div>';
                    var $html = $('<div class="classified"'+infinitescroll+'><a href="'+item.url+'"" target="classified">'+image+ribbon+'</a><div class="caption"><h2 class="left">'+location+'<br/><small><em>'+(item.size?item.size+'m&sup2;':'')+(item.size&&item.rooms?' - ':'')+(item.rooms?(item.rooms>1?item.rooms+' pi&egrave;ces':'studio'):'')+'</em></small></h2><h2 class="right">&euro;'+numberWithCommas(item.price)+'</br><small><i>'+(item.pricepersqm?'('+numberWithCommas(item.pricepersqm)+'/m&sup2;)':'')+'</i></small></h2></div></div>');
  
                    $('#classifieds').append( $html ).isotope( 'insert', $html ).isotope('layout');
                }
                offset+=1;
            }
            $('#infinitescroll').one('inview', function() { feed.display(offset); } );
            this.loading = false;
        },
        sort: function(sortBy) {
            this.loading = true;
            sortOrder = this.sortorder;
            if (sortBy == this.sortby) sortOrder = sortOrder * -1; // if reselecting same sort, flip order
            else if (this.sortby) sortOrder = 1; // if page loaded and changing sort order, return to ascending
            if (sortBy == 'price') { if (sortOrder==-1) this.annonces.sort(function(a, b){return b.price-a.price}); else this.annonces.sort(function(a, b){return a.price-b.price});}
            else if (sortBy == 'pricepersqm') { if (sortOrder==-1) this.annonces.sort(function(a, b){return b.pricepersqm-a.pricepersqm}); else this.annonces.sort(function(a, b){return a.pricepersqm-b.pricepersqm}); }
            else if (sortBy == 'date') { if (sortOrder==-1) this.annonces.sort(function(a, b){return a.date>b.date}); else this.annonces.sort(function(a, b){return a.date<b.date});}
            else if (sortBy == 'pricedrop') { if (sortOrder==-1) this.annonces.sort(function(a, b){return a.pricedrop>b.pricedrop}); else this.annonces.sort(function(a, b){return a.pricedrop<b.pricedrop});}
            this.setproperty('sortby', sortBy);
            this.setproperty('sortorder', sortOrder);
            this.loading = false;
        },
        toggleareas: function(areas) {
            j = areas.length;
            for (i =0; i<j; i++)
            {
                var x = this.locations.indexOf(areas[i]);
                if (x == -1) this.locations.push(areas[i]);
                else this.locations.splice(x,1);
            }
            this.setproperty('areas', JSON.stringify(this.locations));
        },
        setproperty: function(key, value) {
            this[key] = value;
            $.cookie(key, value, { path: '/' });
        },
 
        create: function(el, options) {
            this.locations = options['areas'];
            this.sortorder = options['sortOrder'];
            this.maxprice = options['maxprice'];
            this.maxpricepersqm = options['maxpricepersqm'];
            this.days = options['days']
            var url = 'http://95.85.14.240:8001/json_adverts-'+options['days']+'-days';
            // jQuery AJAX call
            $('#classifieds').loading({ message: 'Loading...' });
            jQuery.ajax({ url: url, cache: false, crossDomain: true, async: false, dataType: 'jsonp', jsonp: "callback", context: this,

                success: function(a){
                    this.annonces = a;
                    this.sort(options['sortBy']);
                    $('#classifieds').loading('stop');
                    this.display(0);
               },
                error: function(xhr, textStatus, errorThrown){
                     alert(textStatus+': '+errorThrown); }
            });
        }
    });
 
    $.fn.classifiedFeed = function(options, callback){
        var d = {};
        this.each(function(){
            var s = $(this);
            d = s.data("classifiedfeed");
            if (!d){
                d = new ClassifiedFeedObject(this, options, callback);
                s.data("classifiedfeed", d);
            }
        });
        return d;
    };
 
    // Function to convert date to relative date
    function nicetime(a){
        var d = Math.round((+new Date - a) / 1000), fuzzy;
        var chunks = new Array();
            chunks[0] = [60 * 60 * 24 * 365 , 'year'];
            chunks[1] = [60 * 60 * 24 * 30 , 'month'];
            chunks[2] = [60 * 60 * 24 * 7, 'week'];
            chunks[3] = [60 * 60 * 24 , 'day'];
            chunks[4] = [60 * 60 , 'hr'];
            chunks[5] = [60 , 'min'];
        var i = 0, j = chunks.length;
        for (i = 0; i < j; i++) {
            s = chunks[i][0];
            n = chunks[i][1];
            if ((xj = Math.floor(d / s)) != 0)
                break;
        }
        fuzzy = xj == 1 ? '1 '+n : xj+' '+n+'s';
        if (i + 1 < j) {
            s2 = chunks[i + 1][0];
            n2 = chunks[i + 1][1];
            if ( ((xj2 = Math.floor((d - (s * xj)) / s2)) != 0) )
                fuzzy += (xj2 == 1) ? ' + 1 '+n2 : ' + '+xj2+' '+n2+'s';
        }
        fuzzy += ' ago';
        return fuzzy;
    }
 
})(jQuery);


function intersect(a, b) {
    var t;
    if (b.length > a.length) t = b, b = a, a = t; // indexOf to loop over shorter
    return a.filter(function (e) {
        if (b.indexOf(e) !== -1) return true;
    });
}
function str2numarr(a)
{
    var x = [];
    x.push.apply(x, a.split(",").map(Number));
    return x;
}
function selectareas(areas)
{
    $('.areabutton').each( function() {
        if (intersect(str2numarr($(this).attr('area')),areas).length > 0) {if ($(this).hasClass('btn-default')) $(this).toggleClass('btn-default btn-success'); }
        else { if ($(this).hasClass('btn-success')) $(this).toggleClass('btn-default btn-success'); }
    });
}
function toggleareas(areas)
{
    feed.toggleareas(str2numarr(areas));
    feed.display(0);    
}
function selectsort(sortby)
{
    var options = ['date','price','pricepersqm','pricedrop'];
    for (i in options)
    {
        if (options[i] == sortby) { if ($( '#sortby'+options[i] ).hasClass('btn-default')) $( '#sortby'+options[i] ).toggleClass('btn-default btn-success'); }
        else if (options[i] != sortby) { if ( $( '#sortby'+options[i] ).hasClass('btn-success')) $( '#sortby'+options[i] ).toggleClass('btn-default btn-success'); }
    }
}
function updatesort(sortby)
{
    selectsort(sortby);
    feed.sort(sortby);
    feed.display(0);
}

