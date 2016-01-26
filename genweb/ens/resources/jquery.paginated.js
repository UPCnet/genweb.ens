/*
 * When applied to an element A, this plugin applies page navigation on its
 * children.
 * The navigation menu is appended to the element with the id specified as the
 * 'navigation' option ('pagination' by default). The number of results per
 * page as well as the maximum number of visible pages of the navigation menu
 * are also configurable via 'resultsPerPage' and 'visiblePages' respectively.
 * This plugin requires the
 * jQuery plugin twbsPagination (http://esimakin.github.io/twbs-pagination/) to
 * be available in order to work.
 *
 * Usage:
 *  $("selector").paginated({
        navigation: "nav_menu",
        resultsPerPage: 20,
        visiblePages: 10}
    });
 */

(function ($)
{
    $.fn.paginated = function(options)
    {
        var paginated_element = $(this);
        var settings = $.extend({
            navigation: 'pagination',
            resultsPerPage: 10,
            visiblePages: 5
        }, options);

        var results_rows = paginated_element.children();
        var results_count = results_rows.length;
        var total_pages = Math.ceil(results_count / settings.resultsPerPage);

        if (total_pages > 0)
        {
            $('#' + settings.navigation).twbsPagination({
                totalPages: total_pages,
                visiblePages: settings.visiblePages,
                first: "<<",
                prev: "<",
                next: ">",
                last: ">>",
                onPageClick: function (event, page)
               {
                    var first_result_index = (page - 1) * settings.resultsPerPage;
                    var last_result_index = Math.min(
                        first_result_index + settings.resultsPerPage, results_count);

                    // Refresh results
                    var page_results = results_rows.slice(
                        first_result_index, last_result_index);
                    paginated_element.children().remove();
                    paginated_element.append(page_results);
                }
            });
        }

        return this;
    };
}(jQuery));
