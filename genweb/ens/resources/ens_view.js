function has_any_historic(container)
{
    results = container.find("input[type=checkbox].selector-td-historic")
    for (i = 0 ; i < results.length ; i ++)
    {
        if (results[i].checked) return true;
    }
    return false;
}

function display_historics(container, show_historics)
{
    container.find("input[type=checkbox].selector-td-historic").each(
        function(index, value)
        {
            if (value.checked)
            {
                if (show_historics)
                {
                    $(value).parent().parent().show("fast");
                }
                else
                {
                    $(value).parent().parent().hide("fast");
                }
            }
        });
}

$(document).ready(function ()
{
    $("#ens-metadata").accordion();

    $("input[type=checkbox].selector-input-historic").each(function(index, value)
    {
        if (has_any_historic($(value).parent()))
        {
            $(value).click(function()
            {
                display_historics($(value).parent(), this.checked);
            });
        }
        else
        {
           $(value).attr('disabled', 'disabled');
        }
    });

    display_historics($(document), false);
});
