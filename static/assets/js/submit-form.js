function initSubmitAppointment() {
    var $form = $("#appointment-form");
    var $nameInput = $("#name");
    var $emailInput = $("#email");
    var $phoneInput = $("#phone");
    var $messageInput = $("#message");

    var $successMessage = $("#successMessage");
    var $errorMessage = $("#errorMessage");

    if ($form.length === 0) {
        return;
    }


    $form.on("submit", function (event) {
        event.preventDefault();

        var isValid = true;

        // Reset invalid states
        $nameInput.removeClass("is-invalid");
        $emailInput.removeClass("is-invalid");
        $phoneInput.removeClass("is-invalid");
        $messageInput.removeClass("is-invalid");

        // Validation rules
        var emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,}$/;
        var phonePattern = /^[0-9+\- ]{6,}$/;

        if ($.trim($nameInput.val()) === "") {
            $nameInput.addClass("is-invalid");
            isValid = false;
        }

        if ($.trim($emailInput.val()) === "" || !emailPattern.test($emailInput.val())) {
            $emailInput.addClass("is-invalid");
            isValid = false;
        }

        if ($.trim($phoneInput.val()) === "" || !phonePattern.test($phoneInput.val())) {
            $phoneInput.addClass("is-invalid");
            isValid = false;
        }

        if ($.trim($messageInput.val()) === "") {
            $messageInput.addClass("is-invalid");
            isValid = false;
        }

        if (!isValid) {
            return;
        }

        // Fake async submission (simulasi)
        setTimeout(function () {
            var success = Math.random() > 0.3;

            if (success) {
                $successMessage.removeClass("d-none");
                $errorMessage.addClass("d-none");
                $form[0].reset();
            } else {
                $successMessage.addClass("d-none");
                $errorMessage.removeClass("d-none");
            }

            // Hide after 5 seconds
            setTimeout(function () {
                $successMessage.addClass("d-none");
                $errorMessage.addClass("d-none");
            }, 5000);

        }, 1000);
    });
}


function initSubmitNewsletter() {
    var $form = $("#newsletter-form");
    var $emailInput = $("#newsletter-email");
    var $successMessage = $("#successMessage-footer");
    var $errorMessage = $("#errorMessage-footer");

    if ($form.length === 0 || $emailInput.length === 0) {
        console.error("Form atau input email tidak ditemukan!");
        return;
    }

    $form.on("submit", function (event) {
        event.preventDefault();

        var isValid = true;
        $emailInput.removeClass("is-invalid");

        var emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
        if ($.trim($emailInput.val()) === "" || !emailPattern.test($emailInput.val())) {
            $emailInput.addClass("is-invalid");
            isValid = false;
        }

        if (!isValid) {
            return;
        }

        setTimeout(function () {
            var success = Math.random() > 0.3;

            if (success) {
                $successMessage.removeClass("d-none");
                $errorMessage.addClass("d-none");
                $form[0].reset();
            } else {
                $successMessage.addClass("d-none");
                $errorMessage.removeClass("d-none");
            }

            setTimeout(function () {
                $successMessage.addClass("d-none");
                $errorMessage.addClass("d-none");
            }, 5000);
        }, 1000);
    });
}