$(document).ready(function()
{
    $("#ens-metadata").accordion({
        collapsible: true,
        active: false
    });
    $("input[type=checkbox].selector-input-historic").hidable_group({
            lang: "ca",
            msg_empty: {"ca": "(No hi ha càrrecs històrics)"}
    });
});
