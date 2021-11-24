
annonces = new FeedObject('http://127.0.0.1:8000/json_private/');

annonces.me = 'annonces';

annonces.all = function(domid, items, options)
{
     options['isotope'] = true;
    options['wrapper_class'] = 'classified';
    var output = [];
    var location,image,ribbon;
    for (i=0; i<items.length; i++)
    {
        item = items[i];
        price = '&euro;'+numberWithCommas(item.price);
        if (item.price > 1000000) price = "<span style=\"font-size: 72%\">"+price+"</span>"
        location = item.location.length>16?"<span style=\"font-size: 72%\">"+item.location+"</span>":item.location;
        image = item.image != ''?'<img width="300" height="225" src="'+item.image+'" alt="" />':'<div style="width:300px;height:225px;overflow:none;">'+item.title+'</div>';
        ribbon = item.pricedrop > 0?'<div class="ribbon-wrapper"><div class="ribbon-inner shadow-pulse bg-warning">'+item.pricedrop+'% Off</div></div>':'';

        output.push({ search: item.search, infinitescroll : item.infinitescroll, html: '<a href="'+item.url+'"" target="classified">'+image+ribbon+'</a><div class="caption"><h2 class="left">'+location+'<br/><small><em>'+(item.size?item.size+'m&sup2;':'')+(item.size&&item.rooms?' - ':'')+(item.rooms?(item.rooms>1?item.rooms+' pi&egrave;ces':'studio'):'')+'</em></small></h2><h2 class="right">'+price+'</br><small><i>'+(item.pricepersqm?'('+numberWithCommas(item.pricepersqm)+'/m&sup2;)':'')+'</i></small></h2></div>' });
    }
    this.list(domid, output, options);
}
