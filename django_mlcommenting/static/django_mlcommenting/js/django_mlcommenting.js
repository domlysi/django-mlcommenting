$(function () {

    // Comments dynamic load with beforeSend preview template
    $('.mlc-comment-element-ajax-wrapper').each(function () {
        load_comment(this)
    });


});

// Comment Post submit - ajax call with result
$(document).on('submit', '#mlc-comment-form', function (e) {
    e.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        method: 'post',
        data: $(this).serialize(),
        context: this,

        beforeSend: function () {

        },
        success: function (data) {
            $('#mlc-comment-success').html(data);
            $(this).parents('.mlc-form-wrapper').fadeOut('slow');
        },
        error: function (data) {
            $('#mlc-comment-success').html("<div class='mlc mlc-message error'>" + data.responseText + "</div>");
        }
    });
});
// Disable Button on no input
$(document).on('change', 'form#mlc-comment-form', function () {
    $(this).find('.mlc-btn[type="submit"]').removeAttr('disabled');
});


function load_comment(obj) {
    let url = $(obj).parents('.mlc-comment-list-wrapper').data('url');
    let preview_url = $(obj).parents('.mlc-comment-list-wrapper').data('preview-url');
    $.ajax({
        url: url,
        context: obj,
        async: true,
        method: 'get',
        data: {
            'comment_id': $(obj).data('commentid'),
        },
        beforeSend: function () {
            $(this).load(preview_url);
        },
        success: function (data) {
            $(this).html(data.html);
        },
        error: function (data) {
            $(this).html(data.responseText.html)
        }
    });
}

// Comment is useful - like
$(document).on('click', '.mlc-comment-like', function () {
    let data = {
        'csrfmiddlewaretoken': $(this).data('csrf'),
        'comment_id': $(this).data('id')
    };

    $.ajax({
        url: $(this).data('url'),
        data: data,
        method: 'post',
        async: true,
        context: $(this),
        beforeSend: function () {

        },
        success: function (data) {
            console.log(data);
            this.toggleClass('active');
            this.find(".mlc-comment-like-count").html(data.likes)
        },
        error: function (xhr, ajaxOptions, thrownError) {

        }
    });
});

// Show original content -- Comment Detail
$(document).on('click', 'a.mlc-comment-translate-show-more', function (e) {
    e.preventDefault();
    $(this).parents('.mlc-translate-origin').find('.mlc-comment-translate-show-more-preview').hide();
    $(this).parents('.mlc-translate-origin').find('.mlc-comment-translate-show-more-content').show();
});


// Load more comments by clicking
$(document).on('click', '.mlc-comments-list-more', function (e) {
    e.preventDefault();
    let url = $(this).attr('href');
    let current = $('.mlc-comment-list-wrapper').data('show-value');

    $.ajax({
        url: url,
        method: 'get',
        data: {
            's': current
        },
        context: this,
        beforeSend: function () {
            $(this).html('loading...')
        },
        success: function (data) {
            let wrapper = $('.mlc-comment-list-wrapper');

            $('.mlc-comments-list-more').remove();

            wrapper.append($(data.html).hide().fadeIn('fast'))
                .data('show-value', current + current);
        },
    });

});


$(document).on('click', '.mlc-delete-post', function (e) {
    e.preventDefault();
    let parent = $(this).parents('.mlc-own-post-wrapper');
    let csrf = parent.data('csrf');
    let url = parent.data('url-delete');

    console.log(csrf);
    console.log(url);

    $.ajax({
        url: url,
        context: parent,
        data: {
            'csrfmiddlewaretoken': csrf,
            'sure': $(this).data('sure'),
        },
        method: 'post',
        success: function (data) {
            if (data.status === "confirm") {
                $(this).find('.mlc-show-own-post').hide();
                $(this).prepend($("<div id='mlc-confirm'>").hide().html(data.html).fadeIn('slow'));
            }
            if (data.status === "deleted") {
                $('#mlc-confirm').remove();
                $(this).append(data.html);
            }
        },
        error: function (data) {
            console.log(data.responseText)
        }

    });
});

$(document).on('click', '.material-icons.mlc-edit-post', function (e) {
    e.preventDefault();
    let container = $(this).parents('.mlc-comment-element-ajax-wrapper').find('.mlc-comment-text--wrapper');
    if (!container.length) {
        container = $(this).parents('#mlc-comment-success').find('.mlc-comment-text--wrapper');
    }

    let text_tmp = container.find('.mlc-comment-text--string').text();

    let textarea = $('<textarea>').text(text_tmp).addClass('mlc-comment-edit--textarea');
    container.html(textarea);
    textarea.focus();

    let save_btn = $('<button>').addClass('mlc mlc-btn').text('Save');
    container.append(save_btn);
});

$(document).on('change blur', '.mlc-comment-edit--textarea', function (e) {
    let container = $(this).parents('.mlc-comment-element-ajax-wrapper').find('.mlc-own-post-wrapper');
    if (!container.length) {
        container = $(this).parents('#mlc-comment-success').find('.mlc-own-post-wrapper');
    }

    if (e.type === 'change') {


        $.ajax({
            url: container.data('url-edit'),
            method: 'post',
            data: {
                'csrfmiddlewaretoken': container.data('csrf'),
                'comment_text': $(this).val(),
            },
            context: this,
            beforeSend: function () {
                $(this).html('saving ...')
            },
            success: function (data) {

            },
        });
    }
    let text = $(this).val();
    let text_span = $('<span>').addClass('mlc-comment-text--string').text(text);
    container = $(this).parents('.mlc-comment-text--wrapper');

    container.html(text_span);
});

