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

    $("input[type=checkbox].selector-input-historic").click(function()
    {
        display_historics($(this).parent(), this.checked);
    });
    display_historics($(document), false);
});
