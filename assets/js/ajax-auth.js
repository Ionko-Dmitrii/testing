$('.form').on('submit', function () {
    let formData = $(this).serialize();
    let url = $(this).attr('action');
    let $this = $(this);
    $this.find('button').attr('disabled', 'disabled');

    $.ajax({
        url: url,
        type: 'post',
        data: formData,

        success: function (data) {
            $this.find('button').removeAttr('disabled');
            $('.invalid-feedback').css('display', 'none').text('');
            new bootstrap.Modal('#exampleModal', {}).show();
            $this[0].reset();
        },

        error: function (errors) {
            $this.find('button').removeAttr('disabled');
            let error_list = errors['responseJSON']['data'];
            jQuery.each(error_list, function (key, value) {
                $(`#${key}`).next('.invalid-feedback').css('display', 'block').text(value[0])
            });
        }
    })
})
const myModalEl = document.getElementById('exampleModal')
myModalEl.addEventListener('hidden.bs.modal', event => {
    window.location.href = window.location.origin
})
