
function numberWithCommas(x) { return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
function short_address(address) { return address.replace('Boulevard', 'Bvd').replace('Avenue', 'Av.').replace(', ', ' '); }

(function($){
 
    OneAgencyFeedObject = function(el, options) {
        this.agents = {};
        this.agencies = {};
        this.create(el, options);
        this.loading = false;
    };
 
    $.extend(OneAgencyFeedObject.prototype, {
 
         display: function(offset) {
            if (this.loading == true) { return; }
            this.loading = true;
            if (offset == 0)
            {
                $('#oneagency').isotope('remove', $('#agents').isotope('getItemElements'));
                $('#oneagency').empty();
            }
            // get agency array from passed id
            for (i=0;i<this.agencies.length;i++) { if (this.agencies[i].agencyid == this.agencyid) { var agency = this.agencies[i]; break; } }
            this.branches = []
            for (i=0;i<this.agencies.length;i++) { if (this.agencies[i].name == agency['name']) { this.branches[this.agencies[i].agencyid] = { 'agency': this.agencies[i], 'agents': [] }; } }
            for (i=0;i<this.agents.length;i++) { if (this.branches[this.agents[i].agencyid]) { this.branches[this.agents[i].agencyid]['agents'].push(this.agents[i]); } }

            for (var key in this.branches) {
                var item = this.branches[key]['agency']; 
                if (item.branch) var branch = '<h5>('+item.branch+')</h5>'; else var branch = '<h5>&nbsp;</h5>';
                var $html = $('<div class="agent" style="color:#000;width:100%" search="'+item.search+'"><h4>'+item.name+'</h4>'+branch+'Téléphone: '+item.telephone+'<br/><br/><a href="'+item.web+'"><i class="fa fa-globe fa-lg"></i></a> <a href="mailto:'+item.email+'"><i class="fa fa-envelope"></i></a> '+short_address(item.address)+' '+item.postcode+' '+item.city+'</div>');
                $('#oneagency').append( $html ).isotope( 'insert', $html ).isotope('layout');
                console.log(item);
                for (var key2 in this.branches[key]['agents']) {
                    item = this.branches[key]['agents'][key2];
                    if (item.mobile) var mobile = 'Téléphone: '+item.mobile+'<br/><br/>'; else var mobile = '';
                    if (item.branch) var branch = ' ('+item.branch+')'; else var branch = '';
                    if (item.email) var email = '<a href="mailto:'+item.email+'"><i class="fa fa-envelope"></i></a> '; else var email = '';
                    var $html = $('<div class="agent"'+' style="color:#000" search="'+item.search+'"><h4>'+item.forename+' '+item.surname+'</h4>'+mobile+email+item.agency+branch+'</div>');
                    $('#oneagency').append( $html ).isotope( 'insert', $html ).isotope('layout');
                    console.log(item);
                }
            }
            this.loading = false;
        },

        setproperty: function(key, value) {
            this[key] = value;
            $.cookie(key, value, { path: '/' });
        },
 
        create: function(el, options) {
            this.agencyid = parseInt(window.location.hash.substring(1));
//            window.location.reload(true);
            var url = '/json_agents/';
            var url_agencies = '/json_agences/';
            // jQuery AJAX call
            if (!this.agencyid) { $('#oneagency').text("No agency id"); return; }
            $('#oneagency').loading({ message: 'Loading agents...' });
//            jQuery.ajax({ url: url, cache: false, crossDomain: true, async: false, dataType: 'jsonp', jsonp: "callback", context: this,
            jQuery.ajax({ url: url, cache: false, crossDomain: false, async: true, dataType: 'json', context: this,

                success: function(a){
                    this.agents = a;
        //            jQuery.ajax({ url: url_agencies, cache: false, crossDomain: true, async: false, dataType: 'jsonp', jsonp: "callback", context: this,
                    jQuery.ajax({ url: url_agencies, cache: false, crossDomain: false, async: true, dataType: 'json', context: this,

                        success: function(a){
                            this.agencies = a;
                            $('#oneagency').loading('stop');
                            this.display(0);
                       },
                        error: function(xhr, textStatus, errorThrown){

                            alert(textStatus+' (agencies): '+errorThrown); }
                    });
               },
                error: function(xhr, textStatus, errorThrown){
                     alert(textStatus+' (agents): '+errorThrown); }
            });
        }
    });
 
    $.fn.oneagencyFeed = function(options, callback){
        var d = {};
        this.each(function(){
            var s = $(this);
            d = s.data("oneagencyfeed");
            if (!d){
                d = new OneAgencyFeedObject(this, options, callback);
                s.data("oneagencyfeed", d);
            }
        });
        return d;
    };

})(jQuery);
