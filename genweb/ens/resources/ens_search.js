$(document).ready(function ()
{
var ens_search_results_url = portal_url + '/ens_searchresults/';

function ens_search()
{
    var input_figura_juridica = $('#search_input_figura_juridica');
    var input_estat = $('#search_input_estat');
    var input_text = $('#search_input_text');
    var button = $('#search_input_button');
    var results = $('#search_results');

    var figura_juridica = input_figura_juridica.val()
    var estat = input_estat.val();
    var text = input_text.val();

    input_figura_juridica.attr('disabled', 'disabled');
    input_estat.attr('disabled', 'disabled');
    input_text.attr('disabled', 'disabled');
    button.attr('disabled', 'disabled');
    $.ajax({
        url: ens_search_results_url,
        data: {figura_juridica: figura_juridica, estat: estat, text: text},
        success: function(data)
        {
            results.html(data);
            input_figura_juridica.removeAttr('disabled');
            input_estat.removeAttr('disabled');
            input_text.removeAttr('disabled');
            button.removeAttr('disabled');
        }
    });
}

$('#search_input_text').on('keydown', function(event)
{
    if (event.keyCode == 13)
    {
        ens_search();
    }
});

$('#search_input_button').on('click', function(event)
{
    ens_search();
});

});
