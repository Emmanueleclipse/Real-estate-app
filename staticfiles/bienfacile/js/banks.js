banks = new FeedObject('/json_banks/');

banks.me = 'banks';

banks.all = function(domid, items, options)
{
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    for (var i=0; i<items.length; i++)
    {
        var item = items[i];
        output.push({ infinitescroll : item.infinitescroll, html: "<td><a href=\"javascript:bankentries.filter('#bankentries', 'bank_account_id', "+item.id+");bankentries.display(0);bankentries.current_account = "+item.id+";bankentries.title('"+item.account_name+"');\">"+item.account_name+'</a></td><td>'+item.bank_name+'</td><td>'+item.bank_address+"</td><td><a href=\"javascript:banks.modal('#modal', { title : 'Modifier banque', hidden: { id: "+item.id+" } });\">"+(item['for']=='agence'?'Agence':'Personelle')+(item.current?' / Actif':'')+'</a></td>' });
    }
    this.list(domid, output, options);
}

banks.form = function()
{
    return [
                { type: 'input', field: 'bank_name', title: 'Nom', required: true },
                { type: 'input', field: 'bank_address', title: 'Adresse', required: true },
                { type: 'input', field: 'account_name', title: 'Nom sur compte', required: true },
                { type: 'textarea', field: 'description', title: 'Descriptif' },
                [
                    [{ type: 'input', field: 'iban', title: 'IBAN' }],
                    [{ type: 'input', field: 'bic', title: 'BIC' }],
                ],
                [
                    [{ type: 'date', field: 'opened_date', title: 'Ouverture' }],
                    [{ type: 'date', field: 'closed_date', title: 'Fermature' }],
                ],
                { type: 'input', field: 'balance', title: 'Solde' },
                [
                    [{ type: 'radio', field: 'for', title: 'Pour', options : { agent: 'Moi', agence: 'Agence'} }],
                    [{ type: 'select2', field: 'agent_id', title: 'Agent', required: true, options: myagency.options('fullname')} ],
                ],
            ];
}

bankentries = new FeedObject('/json_bankentries/');

bankentries.me = 'bankentries';

bankentries.title = function(text)
{
    $('#bankname').text(text);
}

bankentries.all = function(domid, items, options)
{
    var item, html;
    options['isotope'] = false; output = [];
    options['wrapper'] = 'table'; options['wrapper_class'] = 'table table-striped'; options['childwrapper'] = 'tr';
    for (var i=0; i<items.length; i++)
    {
        item = items[i];
        html = concat_cells({ 'cell_open' : "<td><a href=\"javascript:bankentries.modal('#modal', { title : 'Modifier', hidden: { id: "+item.id+", 'bank_account_id' : "+item.bank_account_id+" } });\">", 'cell_close': '</a></td>', 'cells' : [item.date, '&euro;'+item.amount, item.reference, item.comment] });
        output.push({ 'search': (item.comment?item.comment.toLowerCase():'')+' '+(item.reference?item.reference.toLowerCase():''), infinitescroll : item.infinitescroll, html: html });
    }
    this.list(domid, output, options);
}

bankentries.form = function()
{
    return [
                [
                    [{ type: 'input', field: 'reference', title: 'Reference' }],
                    [{ type: 'input', field: 'comment', title: 'Motif' }],
                ],
                [
                    [{ type: 'input', field: 'amount', title: 'Montant', required: true }],
                    [{ type: 'date', field: 'date', title: 'Date' }],
                ],
            ];
}

bankentries.upload = function(domid, options)
{
    if (!options) var options = {}; if (!options['hidden']) options['hidden'] = {};
    options['hidden']['csrfmiddlewaretoken'] = window.csrf;
    options['header'] = '<div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Fermer"><span aria-hidden="true">&times;</span></button><h4 class="modal-title">'+(options['title']?options['title']:'Missing title')+'</h4></div><div class="modal-body">';
    options['footer'] = '</div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>';
    if (!options['hidden']['bank_account_id']) options['bodytop'] = "Choisir une banque"; else 
    options['bodytop'] = '<div id="drag-drop-area"></div><div class="uppy-ProgressBar"></div>'+
                          "<script>var uppy = Uppy.Core( { autoProceed: true, logger: Uppy.debugLogger, debug: true } );"+
                          "uppy.use(Uppy.DragDrop, { target: '#drag-drop-area' });"+
                          "uppy.use(Uppy.XHRUpload, { endpoint: 'https://agence.bienfacile.com/json_bankupload/' });"+
                          "uppy.on('upload-success', (file,response) => { if (response.body['success']) $('"+domid+"form_results').append(response.body['success']+'<br/>'); if (response.body['error']) $('"+domid+"form_errors').append(response.body['error']+'<br/>'); bankentries.display()});"+
                          "uppy.use(Uppy.ProgressBar, { target: '.uppy-ProgressBar', hideAfterFinish: true });"+
                          "uppy.on('upload-error', (file, error, response) => $('"+domid+"form_errors').append('File: '+file.id+' - '+error));"+
                          "uppy.use(Uppy.Form, { target: '"+domid+"form', getMetaFromForm: true });"+
                          "</script>";

    var modal = $(domid), form = {};
    modal.find('.modal-content').html(this.renderform(domid, form, options));
    this.forminitialise(domid, true, form);
    modal.modal('show');
}