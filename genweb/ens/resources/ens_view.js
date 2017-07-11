$(document).ready(function()
{
    $("#ens-metadata").accordion({
        collapsible: true,
        active: false,
        heightStyle: 'content'
    });

    $("input[type=checkbox].selector-input-historic").hidable_group({
            lang: "ca",
            msg_empty: {"ca": "(No hi ha càrrecs històrics)"}
    });

    $("input.composicio-switch").each(function(index, item)
    {
        function display(checkbox)
        {
            if (checkbox.prop('checked'))
            {
                checkbox.next().next().show();
            }
            else
            {
                checkbox.next().next().hide();
            }
        }
        if ($(this).next().next().html() == '')
        {
            $(this).parent().css('display', 'none');
        }
        else
        {
            $(item).click(function(){display($(item))});
            display($(item));
        }
    });

    $("input[type=checkbox].selector-input-observacions").change(function() {
        if(this.checked) {
            $(".observacions-content").css('display', 'block');
        }
        else {
            $(".observacions-content").css('display', 'none');
        }
    });

});
