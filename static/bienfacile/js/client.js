
function load_clientdetails(divid)
{
    var url = '/json_clients/';
    jQuery.ajax({ url: url, cache: false, crossDomain: false, async: true, dataType: 'json', context: this,

                success: function(a){
                    $(divid).text(a[client.id]);
               },
                error: function(xhr, textStatus, errorThrown){
                     alert(textStatus+': '+errorThrown); }
            });

}
