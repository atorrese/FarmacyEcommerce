    // Remember? You generated the client token in your view.
    var braintree_client_token = "{{ braintree_client_token }}";

    requirejs(['jquery', 'jsi18n', 'https://js.braintreegateway.com/js/braintree-2.28.0.min.js'], function($, jsi18n, braintree) {
        function braintreeSetup() {
            // Here you tell Braintree to add the drop-in to your division above
            braintree.setup(braintree_client_token, "dropin", {
                container: "braintree-dropin"
                ,onError: function (obj) {
                    // Errors will be added to the html code
                    $('[type=submit]').prop('disabled', false);
                    $('.braintree-notifications').html('<p class="alert alert-danger">' + obj.message + '</p>');
                }
            });
        }
        braintreeSetup();
        $('form').submit(function () {
            $('[type=submit]').prop('disabled', true);
            $('.braintree-notifications').html('');
        });
    });