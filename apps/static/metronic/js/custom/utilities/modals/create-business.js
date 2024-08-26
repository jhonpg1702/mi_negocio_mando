"use strict";

// Definición de la clase
var KTCreateAccount = function () {
	// Elementos
	var modal;	
	var modalEl;

	var stepper;
	var form;
	var formSubmitButton;
	var formContinueButton;
	var formPreviousButton;

	// Variables
	var stepperObj;
	var validations = [];

	// Funciones privadas
	var initStepper = function () {
		// Inicializar el Stepper
		stepperObj = new KTStepper(stepper);
		console.log(stepperObj.getCurrentStepIndex())
		// Evento de cambio en el Stepper
		if (stepperObj.getCurrentStepIndex() === 1) {
			formSubmitButton.classList.remove('d-none');
			formSubmitButton.classList.add('d-inline-block');
			formContinueButton.classList.add('d-none');
		} 
		stepperObj.on('kt.stepper.changed', function (stepper) {
			
	
				formSubmitButton.classList.add('d-none');
				formContinueButton.classList.add('d-none');
				formPreviousButton.classList.add('d-none');
			
		});

		// Validación antes de pasar a la siguiente página
		stepperObj.on('kt.stepper.next', function (stepper) {
			console.log('stepper.next');
			// Validar el formulario antes de cambiar el paso del Stepper
			var validator = validations[stepper.getCurrentStepIndex() - 1]; // obtener el validador para el paso actual

			if (validator) {
				validator.validate().then(function (status) {
					console.log('¡validado!');

					if (status == 'Valid') {
						stepper.goNext();

						KTUtil.scrollTop();
					} else {
						Swal.fire({
							text: "Lo sentimos, parece que se han detectado algunos errores. Por favor, inténtalo de nuevo.",
							icon: "error",
							buttonsStyling: false,
							confirmButtonText: "¡Ok, entendido!",
							customClass: {
								confirmButton: "btn btn-light"
							}
						}).then(function () {
							KTUtil.scrollTop();
						});
					}
				});
			} else {
				stepper.goNext();

				KTUtil.scrollTop();
			}
		});

		// Evento de paso anterior
		stepperObj.on('kt.stepper.previous', function (stepper) {
			console.log('stepper.previous');

			stepper.goPrevious();
			KTUtil.scrollTop();
		});
	}

	var handleForm = function() {
		formSubmitButton.addEventListener('click', function (e) {
			// Validar el formulario antes de cambiar el paso del Stepper
			var validator = validations[0]; // obtener el validador para el último formulario
	
			validator.validate().then(function (status) {
				console.log('¡validado!');
	
				if (status == 'Valid') {
					// Prevenir la acción predeterminada del botón
					e.preventDefault();
	
					// Deshabilitar el botón para evitar múltiples clics 
					formSubmitButton.disabled = true;
	
					// Mostrar indicador de carga
					formSubmitButton.setAttribute('data-kt-indicator', 'on');
	
					// Crear objeto FormData desde el formulario
					var form = $('#kt_create_account_form');
					var formData = form.serialize(); // serializar el formulario
	
					// Obtener el token CSRF desde el meta tag
					// var csrfToken = $('meta[name="csrf-token"]').attr('content');
	
					// Enviar el formulario usando AJAX
					$.ajax({
						type: "POST",
						url: form.attr('action'),
						data: formData,
						// headers: {
						// 	'X-CSRFToken': csrfToken  // Añadir el token CSRF al encabezado
						// },
						success: function(data) {
							if (data.success) {
		
								// Avanzar al siguiente paso del stepper
								stepperObj.goNext();

								Swal.fire({
									title: 'Éxito',
									text: data.message,
									icon: 'success',
									confirmButtonText: 'OK'
								});
								
							} else {
								Swal.fire({
									title: 'Error',
									text: data.message,
									icon: 'error',
									confirmButtonText: 'OK'
								});
							}
							// Ocultar indicador de carga
							formSubmitButton.removeAttribute('data-kt-indicator');
							// Habilitar el botón
							formSubmitButton.disabled = false;
						},
						error: function(xhr, status, error) {
							// Manejar errores de respuesta
							Swal.fire({
								text: "Lo sentimos, hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.",
								icon: "error",
								buttonsStyling: false,
								confirmButtonText: "¡Ok, entendido!",
								customClass: {
									confirmButton: "btn btn-light"
								}
							}).then(function () {
								KTUtil.scrollTop();
							});
	
							// Ocultar indicador de carga
							formSubmitButton.removeAttribute('data-kt-indicator');
	
							// Habilitar el botón
							formSubmitButton.disabled = false;
						}
					});
	
				} else {
					Swal.fire({
						text: "Lo sentimos, parece que se han detectado algunos errores. Por favor, inténtalo de nuevo.",
						icon: "error",
						buttonsStyling: false,
						confirmButtonText: "¡Ok, entendido!",
						customClass: {
							confirmButton: "btn btn-light"
						}
					}).then(function () {
						KTUtil.scrollTop();
					});
				}
			});
		});
	}

	var initValidation = function () {
		// Inicializar las reglas de validación del formulario. Para más información, consulta la documentación oficial del plugin FormValidation: https://formvalidation.io/
		// Paso 1
		validations.push(FormValidation.formValidation(
			form,
			{
				fields: {
					'business_name': {
						validators: {
							notEmpty: {
								message: 'El nombre del negocio es obligatorio'
							}
						}
					},

					'business_type': {
						validators: {
							notEmpty: {
								message: 'El tipo de negocio es obligatorio'
							}
						}
					},
					'business_email': {
						validators: {
							notEmpty: {
								message: 'El correo electrónico del negocio es obligatorio'
							},
							emailAddress: {
								message: 'El valor no es una dirección de correo electrónico válida'
							}
						}
					}
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					// Integración con el Framework Bootstrap
					bootstrap: new FormValidation.plugins.Bootstrap5({
						rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
					})
				}
			}
		));
	}

	return {
		// Funciones públicas
		init: function () {
			// Elementos
			modalEl = document.querySelector('#kt_modal_create_account');

			if (modalEl) {
				modal = new bootstrap.Modal(modalEl);	
			}					

			stepper = document.querySelector('#kt_create_account_stepper');

			if (!stepper) {
				return;
			}

			form = stepper.querySelector('#kt_create_account_form');
			formSubmitButton = stepper.querySelector('[data-kt-stepper-action="submit"]');
			formContinueButton = stepper.querySelector('[data-kt-stepper-action="next"]');
			formPreviousButton = stepper.querySelector('[data-kt-stepper-action="previous"]');

			initStepper();
			initValidation();
			handleForm();
		}
	};
}();

// Al cargar el documento
KTUtil.onDOMContentLoaded(function() {
    KTCreateAccount.init();
});
