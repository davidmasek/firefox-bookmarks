const to_remove = new Set();

$(function () { 
    $(".tree-node").each((i, dom_el) => {
        const node = $(dom_el);
        const guid = node.data('guid');
        const url = node.attr('href');
        // console.log(guid, url);
        const btn = $('<button type="button" class="btn btn-outline-danger btn-sm"><i class="fa fa-times"></i></button>')
        btn.css('margin-left', '5px');
        btn.on('click', () => {
            node.toggleClass('remove-this');
            if (node.hasClass('remove-this')) {
                node.css('text-decoration', 'line-through');
                node.css('color', 'red');
                to_remove.add(guid);
            } else {
                node.css('text-decoration', '');
                node.css('color', '');
                to_remove.delete(guid);
            }
        });
        node.after(btn);
    });

    $("#export").on('click', () => {
        console.log(to_remove);
        const els = [];
        to_remove.forEach(el => {
            els.push(el);
        });
        $("#export-data").text(els);
        $("#export-data-container").collapse('show');
    });
});