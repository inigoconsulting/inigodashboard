(function () {
    $.fn.load_data_url = function (url) {
        if (!url) {
            var url = $(this).attr('data-url');
        }
        $(this).html($('#ajax-loader').html());
        $(this).load(url);
    }
    $(document).ready(function () {
        $('#pane').load_data_url();
        $('body').on('click', '.pane-url', function (ev) {
            $('#pane').load_data_url($(this).attr('href'));
            ev.preventDefault();
            return false;
        });
    });
})()
