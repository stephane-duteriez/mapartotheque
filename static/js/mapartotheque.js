function search() {
    var name = $("#searchItem").val();
    var selection = $("p:contains('" + name + "'):first");
    if (selection.length !== 0) {
        if (selection.is(":hidden"))
        {
            selection.parent().parent().parent().parent().prev().click();
        }
        $('html, body').animate({
            scrollTop: selection.offset().top - 100
        }, 1000);
    } else {
        alert("didn't find anything!")
    }
};

$(document).ready(function() {
    to_execute();
    navigator.serviceWorker.register('static/js/service-worker.js');
});
