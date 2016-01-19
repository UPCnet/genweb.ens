var results_per_page = 10;

$(document).ready(function ()
{
    var results_rows = $('#results tbody tr');
    var results_count = results_rows.length;
    var total_pages = Math.ceil(results_count / results_per_page);

    $('#pagination').twbsPagination({
        totalPages: total_pages,
        visiblePages: 5,
        first: "<<",
        prev: "<",
        next: ">",
        last: ">>",
        onPageClick: function (event, page)
        {
            var first_result_index = (page - 1) * results_per_page;
            var last_result_index = Math.min(first_result_index + results_per_page, results_count);

            // Refresh results
            var page_results = results_rows.slice(first_result_index, last_result_index);
            $('#results tbody tr').remove();
            $('#results tbody').append(page_results);
        }
    });
});
