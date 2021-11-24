
myagency = new FeedObject('/json_monagence/');

myagency.load(false);
/* yagency.fullname = function(a)
{
    if (!a) return "noname";
    return a['forename']+' '+a['surname'];
}

myagency.options = function()
{
    var options = {};
    for (var i=0; i<this.data.length; i++) options[this.data[i]['id']] = this.fullname(this.data[i]);
    return options;
}
*/
myagency.staff = function(id)
{
    var arr = this.getdata(id);
    return this.fullname(arr);
}

myagency.me = 'myagency';
