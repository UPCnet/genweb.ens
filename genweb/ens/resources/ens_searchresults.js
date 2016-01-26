var results_per_page = 10;
var visible_pages = 5;

$(document).ready(function ()
{
    $('#results').paginated({
       navigation: 'pagination',
       resultsPerPage: results_per_page,
       visiblePages: visible_pages 
    });
});
