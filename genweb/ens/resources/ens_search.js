var ens_search_results_url = portal_url + '/ens_search_results/';

function ens_search()
{
    var input_figura_juridica = $('#search_input_figura_juridica');
    var input_estat = $('#search_input_estat');
    var input_text = $('#search_input_text');
    var input_carpetes = $('#search_input_carpetes');
    var button = $('#search_input_button');
    var results = $('#search_results');

    var figura_juridica = input_figura_juridica.val()
    var estat = input_estat.val();
    var carpetes = input_carpetes.val();
    var text = input_text.val();

    input_figura_juridica.attr('disabled', 'disabled');
    input_estat.attr('disabled', 'disabled');
    input_text.attr('disabled', 'disabled');
    input_carpetes.attr('disabled', 'disabled');
    button.attr('disabled', 'disabled');
    $.ajax({
        url: ens_search_results_url,
        data: {figura_juridica: figura_juridica, estat: estat,
               carpetes: JSON.stringify(carpetes), text: text},
        success: function(data)
        {
            results.html(data);
            input_figura_juridica.removeAttr('disabled');
            input_estat.removeAttr('disabled');
            input_carpetes.removeAttr('disabled');
            input_text.removeAttr('disabled');
            button.removeAttr('disabled');
        }
    });
}

function apply_filter_to_link(link)
{
    link.click(function()
    {
        var carpetes = $('#search_input_carpetes').val();
        if (carpetes != null)
        {
            var base_url = link.attr('href').split('?')[0];
            var filter_url = base_url + '?carpetes=' + JSON.stringify(carpetes);
            window.location.href = filter_url;
            return false;
        }
    });
}

$(document).ready(function ()
{
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

    apply_filter_to_link($('#link_taula_identificativa'));
    apply_filter_to_link($('#link_taula_representacio'));

    ens_search();
});
