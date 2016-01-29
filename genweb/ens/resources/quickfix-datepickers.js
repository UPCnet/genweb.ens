/*
 * Quickfix: Overrides date pickers year interval with [1900, current + 10].
 * Please, remove this and code it gracefully in the backend if you dare.
 */
$(document).ready(function ()
{
var oldest_year = 1900;
var latest_year = 2030;
// Disable jQuery dateinput plugin
$.fn.dateinput = null;

$('select.year').each(function(index, elem)
{
    var selected_year = $(elem).find('option[selected]').val();
    $(elem).children().remove();
    $(elem).append('<option value="">--</option>');
    for (var year = latest_year; year >= oldest_year; year --)
    {
        var selected_html = year == selected_year ? 'selected' : '';
        var new_option_html = '<option value="' + year + '"' +
                              selected_html + '>' + year + '</option>';
        $(elem).append(new_option_html);
    }
});
});
