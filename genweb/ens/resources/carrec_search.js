var carrec_search_results_url = portal_url + '/carrec_search_results/';

function carrec_search()
{
    var input_text = $('#search_input_text');
    var input_carpetes = $('#search_input_carpetes');
    var input_historics = $('#search_input_historics');
    var button = $('#search_input_button');
    var results = $('#search_results');

    var text = input_text.val();
    var carpetes = input_carpetes.val();
    var historics = input_historics.attr('checked') ? true : false;

    input_text.attr('disabled', 'disabled');
    input_carpetes.attr('disabled', 'disabled');
    input_historics.attr('disabled', 'disabled');
    button.attr('disabled', 'disabled');
    $.ajax({
        url: carrec_search_results_url,
        data: {text: text, carpetes: JSON.stringify(carpetes), historics: historics},
        success: function(data)
        {
            results.html(data);
            input_text.removeAttr('disabled');
            input_carpetes.removeAttr('disabled');
            input_historics.removeAttr('disabled');
            button.removeAttr('disabled');
        }
    });
}

$(document).ready(function ()
{
    $('#search_input_text').on('keydown', function(event)
    {
        if (event.keyCode == 13)
        {
            carrec_search();
        }
    });

    $('#search_input_button').on('click', function(event)
    {
        carrec_search();
    });
});
