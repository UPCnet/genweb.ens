/*
 * When applied to a checkbox A, this plugin configures A so that, when
 * checked/unchecked, it shows/hides a set of DOM elements. The elements to
 * show/hide are the grandparents of the elements matching the following
 * criteria:
 *   - are in the progeny of the A's parent,
 *   - are input elements with checkbox type,
 *   - are checked,
 *   - are marked with the CSS class '.hidable-group-element'.
 * In case there are no elements matching the above criteria, the text set in
 * the 'msg_empty' option is showed as the text of the label defined for A.
 *
 * Usage:
 *  $("selector").hidable_group({
        lang: "ca",
        msg_empty: {"ca", "(No hi ha càrrecs històrics)"}
    });
 */

(function ($)
{
    function has_any_hidden_element(container)
    {
        results = container.find("input[type=checkbox].hidable-group-element")
        for (i = 0 ; i < results.length ; i ++)
        {
            if (results[i].checked) return true;
        }
        return false;
    }

    function display_hidden_elements(container, show_hidden_elements)
    {
        container.find("input[type=checkbox].hidable-group-element").each(
            function(index, value)
            {
                if (value.checked)
                {
                    if (show_hidden_elements)
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

    $.fn.hidable_group = function(options)
    {
        var settings = $.extend({
            lang: "ca",
            msg_empty: {"ca": "(No hi ha elements ocults)"}
        }, options);

        this.each(function(index, value)
        {
            if (has_any_hidden_element($(value).parent()))
            {
                $(value).click(function()
                {
                    display_hidden_elements($(value).parent(), this.checked);
                });
                display_hidden_elements($(value).parent(), false);
            }
            else
            {
                $(value).css('display', 'none');
                $(value).parent().find(
                    "label[for=" + $(value).attr('id') + "]").text(
                        settings['msg_empty'][settings.lang]);
            }
        });

        return this;
    };
}(jQuery));
