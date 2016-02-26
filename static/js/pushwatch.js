$(document).ready(function(){
    $('#id_gcm_data').parent().hide();
    $('#id_apns_data').parent().hide();
    $('#cta').on('click', function(){
        var $splitter = $('.splitter');
        if ($splitter.hasClass('showing')) {
            $splitter.removeClass('showing');
        } else {
            $splitter.addClass('showing');
        }
    });
    $('input#id_use_json:checkbox').on('change', function(){
        console.log('changed');
        if ($(this).is(':checked')){
            console.log('checked');
            $('#id_gcm_data').parent().show();
            $('#id_apns_data').parent().show();
            $('#id_gcm_message').parent().hide();
            $('#id_apns_message').parent().hide();
        } else {
            console.log('unchecked');
            $('#id_gcm_data').parent().hide();
            $('#id_apns_data').parent().hide();
            $('#id_gcm_message').parent().show();
            $('#id_apns_message').parent().show();
        }
    });
});
