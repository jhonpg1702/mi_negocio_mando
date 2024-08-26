"use strict";

// Class definition
var KTSignupGeneral = function () {
    // Elements
    var form;
    var submitButton;
    var validator;
    var passwordMeter;

    // Handle form
    // var handleForm = function (e) {
    //     // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
    //     validator = FormValidation.formValidation(
    //         form,
    //         {
    //             fields: {
    //                 'username': {  // Añadir la validación del campo username
    //                     validators: {
    //                         notEmpty: {
    //                             message: 'El nombre de usuario es obligatorio'
    //                         },
    //                         stringLength: {
    //                             min: 4,
    //                             max: 20,
    //                             message: 'El nombre de usuario debe tener entre 4 y 20 caracteres'
    //                         }
    //                     }
    //                 },
    //                 'phone': {  // Añadir la validación del campo teléfono
    //                     validators: {
    //                         notEmpty: {
    //                             message: 'El número de teléfono es obligatorio'
    //                         },
    //                         regexp: {
    //                             regexp: /^[0-9]{10,10}$/,
    //                             message: 'El número de teléfono debe contener 10 dígitos y solo números'
    //                         }
    //                     }
    //                 },
    //                 'email': {
    //                     validators: {
    //                         regexp: {
    //                             regexp: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    //                             message: 'El valor no es una dirección de correo válida',
    //                         },
    //                         notEmpty: {
    //                             message: 'La dirección de correo es obligatoria'
    //                         }
    //                     }
    //                 },
    //                 'password': {
    //                     validators: {
    //                         notEmpty: {
    //                             message: 'La contraseña es obligatoria'
    //                         },
    //                         callback: {
    //                             message: 'Por favor ingrese una contraseña válida',
    //                             callback: function (input) {
    //                                 if (input.value.length > 0) {
    //                                     return validatePassword();
    //                                 }
    //                             }
    //                         }
    //                     }
    //                 },
    //                 'confirm-password': {
    //                     validators: {
    //                         notEmpty: {
    //                             message: 'La confirmación de la contraseña es obligatoria'
    //                         },
    //                         identical: {
    //                             compare: function () {
    //                                 return form.querySelector('[name="password"]').value;
    //                             },
    //                             message: 'La contraseña y su confirmación no coinciden'
    //                         }
    //                     }
    //                 },
    //                 'toc': {
    //                     validators: {
    //                         notEmpty: {
    //                             message: 'Debes aceptar los términos y condiciones'
    //                         }
    //                     }
    //                 }
    //             },
    //             plugins: {
    //                 trigger: new FormValidation.plugins.Trigger({
    //                     event: {
    //                         password: false
    //                     }
    //                 }),
    //                 bootstrap: new FormValidation.plugins.Bootstrap5({
    //                     rowSelector: '.fv-row',
    //                     eleInvalidClass: '',  // comente para habilitar los iconos de estado inválido
    //                     eleValidClass: '' // comente para habilitar los iconos de estado válido
    //                 })
    //             }
    //         }
    //     );

    //     // Handle form submit
    //     submitButton.addEventListener('click', function (e) {
    //         e.preventDefault();

    //         validator.revalidateField('password');

    //         validator.validate().then(function (status) {
    //             if (status == 'Valid') {
    //                 // Show loading indication
    //                 submitButton.setAttribute('data-kt-indicator', 'on');

    //                 // Disable button to avoid multiple click
    //                 submitButton.disabled = true;

    //                 // Simulate ajax request
    //                 setTimeout(function () {
    //                     // Hide loading indication
    //                     submitButton.removeAttribute('data-kt-indicator');

    //                     // Enable button
    //                     submitButton.disabled = false;

    //                     // Show message popup. For more info check the plugin's official documentation: https://sweetalert2.github.io/
    //                     Swal.fire({
    //                         text: "You have successfully reset your password!",
    //                         icon: "success",
    //                         buttonsStyling: false,
    //                         confirmButtonText: "¡Ok, lo tengo!",
    //                         customClass: {
    //                             confirmButton: "btn btn-primary"
    //                         }
    //                     }).then(function (result) {
    //                         if (result.isConfirmed) {
    //                             form.reset();  // reset form
    //                             passwordMeter.reset();  // reset password meter
    //                             //form.submit();

    //                             //form.submit(); // submit form
    //                             var redirectUrl = form.getAttribute('data-kt-redirect-url');
    //                             if (redirectUrl) {
    //                                 location.href = redirectUrl;
    //                             }
    //                         }
    //                     });
    //                 }, 1500);
    //             } else {
    //                 // Show error popup. For more info check the plugin's official documentation: https://sweetalert2.github.io/
    //                 Swal.fire({
    //                     text: "Lo sentimos, parece que se detectaron algunos errores, por favor inténtalo de nuevo.",
    //                     icon: "error",
    //                     buttonsStyling: false,
    //                     confirmButtonText: "¡Ok, lo tengo!",
    //                     customClass: {
    //                         confirmButton: "btn btn-primary"
    //                     }
    //                 });
    //             }
    //         });
    //     });

    //     // Handle password input
    //     form.querySelector('input[name="password"]').addEventListener('input', function () {
    //         if (this.value.length > 0) {
    //             validator.updateFieldStatus('password', 'NotValidated');
    //         }
    //     });
    // }


    // Handle form ajax
    var handleFormAjax = function (e) {
        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    'username': {  // Añadir la validación del campo username
                        validators: {
                            notEmpty: {
                                message: 'El nombre de usuario es obligatorio'
                            },
                            stringLength: {
                                min: 4,
                                max: 20,
                                message: 'El nombre de usuario debe tener entre 4 y 20 caracteres'
                            }
                        }
                    },
                    'phone': {  // Añadir la validación del campo teléfono
                        validators: {
                            notEmpty: {
                                message: 'El número de teléfono es obligatorio'
                            },
                            regexp: {
                                regexp: /^[0-9]{10,10}$/,
                                message: 'El número de teléfono debe contener 10 dígitos y solo números'
                            }
                        }
                    },
                    'email': {
                        validators: {
                            regexp: {
                                regexp: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                                message: 'El valor no es una dirección de correo válida',
                            },
                            notEmpty: {
                                message: 'La dirección de correo es obligatoria'
                            }
                        }
                    },
                    'password': {
                        validators: {
                            notEmpty: {
                                message: 'La contraseña es obligatoria'
                            },
                            callback: {
                                message: 'Por favor ingrese una contraseña válida',
                                callback: function (input) {
                                    if (input.value.length > 0) {
                                        return validatePassword();
                                    }
                                }
                            }
                        }
                    },
                    'confirm-password': {
                        validators: {
                            notEmpty: {
                                message: 'La confirmación de la contraseña es obligatoria'
                            },
                            identical: {
                                compare: function () {
                                    return form.querySelector('[name="password"]').value;
                                },
                                message: 'La contraseña y su confirmación no coinciden'
                            }
                        }
                    },
                    'toc': {
                        validators: {
                            notEmpty: {
                                message: 'Debes aceptar los términos y condiciones'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger({
                        event: {
                            password: false
                        }
                    }),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',  // comente para habilitar los iconos de estado inválido
                        eleValidClass: '' // comente para habilitar los iconos de estado válido
                    })
                }
            }
        );
        // Configurar Axios para incluir el token CSRF en las solicitudes
        axios.defaults.headers.common['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        // Handle form submit
        submitButton.addEventListener('click', function (e) {
            e.preventDefault();
        
            validator.revalidateField('password');
        
            validator.validate().then(function (status) {
                if (status == 'Valid') {
                    // Mostrar indicación de carga
                    submitButton.setAttribute('data-kt-indicator', 'on');
        
                    // Deshabilitar botón para evitar múltiples clics
                    submitButton.disabled = true;
        
                    // Realizar solicitud POST usando axios
                    axios.post(submitButton.closest('form').getAttribute('action'), new FormData(form))
                        .then(function (response) {
                            if (response.data.success) {
                                form.reset();
        
                                const redirectUrl = form.getAttribute('data-kt-redirect-url');
                                if (redirectUrl) {
                                    location.href = redirectUrl;
                                }
                            } else {
                                Swal.fire({
                                    text: response.data.message || "Lo sentimos, parece que se detectaron algunos errores, por favor inténtalo de nuevo.",
                                    icon: "error",
                                    buttonsStyling: false,
                                    confirmButtonText: "¡Ok, lo tengo!",
                                    customClass: {
                                        confirmButton: "btn btn-primary"
                                    }
                                });
                            }
                        })
                        .catch(function (error) {
                            Swal.fire({
                                text: "Lo sentimos, parece que se detectaron algunos errores, por favor inténtalo de nuevo.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "¡Ok, lo tengo!",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            });
                        })
                        .then(() => {
                            // Ocultar indicación de carga
                            submitButton.removeAttribute('data-kt-indicator');
        
                            // Habilitar botón
                            submitButton.disabled = false;
                        });
                } else {
                    Swal.fire({
                        text: "Lo sentimos, parece que se detectaron algunos errores, por favor inténtalo de nuevo.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "¡Ok, lo tengo!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    });
                }
            });
        });
        
        // Handle password input
        form.querySelector('input[name="password"]').addEventListener('input', function () {
            if (this.value.length > 0) {
                validator.updateFieldStatus('password', 'NotValidated');
            }
        });
    }


    // Password input validation
    var validatePassword = function () {
        return (passwordMeter.getScore() > 50);
    }

    // var isValidUrl = function(url) {
    //     try {
    //         new URL(url);
    //         return true;
    //     } catch (e) {
    //         return false;
    //     }
    // }

    // Public functions
    return {
        // Initialization
        init: function () {
            // Elements
            form = document.querySelector('#kt_sign_up_form');
            submitButton = document.querySelector('#kt_sign_up_submit');
            passwordMeter = KTPasswordMeter.getInstance(form.querySelector('[data-kt-password-meter="true"]'));

            handleFormAjax();

            // if (isValidUrl(submitButton.closest('form').getAttribute('action'))) {
            //     handleFormAjax();
            // } else {
            //     handleForm();
            // }
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTSignupGeneral.init();
});
