odoo.define('location_tracker.geolocation', function (require) {
    "use strict";

    var core = require('web.core');
    var rpc = require('web.rpc');
    var session = require('web.session'); // Para obtener info de la sesión si es necesario

    var _t = core._t;
    var intervalId = null;
    var trackingInterval = 10000; // 10 segundos en milisegundos

    function sendLocationToServer(position) {
        var coords = position.coords;
        console.log("Sending location:", coords.latitude, coords.longitude);

        rpc.query({
            route: '/save_location',
            params: {
                latitude: coords.latitude,
                longitude: coords.longitude,
                accuracy: coords.accuracy // Opcional: enviar precisión
            },
        }).then(function (result) {
            if (result.status === 'success') {
                console.log('Location successfully saved by server.');
            } else {
                console.error('Server error saving location:', result.message);
                // Podrías detener el tracking si hay errores persistentes
                // stopGeolocationTracking();
            }
        }).catch(function (error) {
            console.error('RPC Error sending location:', error);
            // Podrías detener el tracking en caso de error de red/RPC
            // stopGeolocationTracking();
        });
    }

    function errorCallback(error) {
        console.warn(`ERROR(${error.code}): ${error.message}`);
        // Podrías informar al usuario o detener el tracking
        switch (error.code) {
            case error.PERMISSION_DENIED:
                console.error("User denied the request for Geolocation.");
                // Detener futuros intentos si el permiso es denegado
                stopGeolocationTracking();
                break;
            case error.POSITION_UNAVAILABLE:
                console.error("Location information is unavailable.");
                break;
            case error.TIMEOUT:
                console.error("The request to get user location timed out.");
                break;
            case error.UNKNOWN_ERROR:
                console.error("An unknown error occurred.");
                break;
        }
    }

    function startGeolocationTracking() {
        if (navigator.geolocation) {
            // Detener cualquier intervalo previo por si acaso
            if (intervalId !== null) {
                clearInterval(intervalId);
            }

            // Obtener la posición inmediatamente al inicio
            navigator.geolocation.getCurrentPosition(sendLocationToServer, errorCallback, {
                enableHighAccuracy: true, // Intenta obtener la mejor precisión posible
                timeout: 10000,         // Tiempo máximo para obtener la posición (10s)
                maximumAge: 0           // No usar caché de posición
            });


            // Establecer el intervalo para obtener la posición cada 10 segundos
            intervalId = setInterval(function() {
                navigator.geolocation.getCurrentPosition(sendLocationToServer, errorCallback, {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                });
            }, trackingInterval);

            console.log("Geolocation tracking started.");

            // ¡Importante! Solicitar permiso al usuario y explicar por qué
            // El navegador lo hará automáticamente la primera vez, pero es buena práctica
            // tener una UI que explique por qué se pide la ubicación.

        } else {
            console.error("Geolocation is not supported by this browser.");
            alert(_t("Geolocation is not supported by this browser. Location tracking disabled."));
        }
    }

    function stopGeolocationTracking() {
        if (intervalId !== null) {
            clearInterval(intervalId);
            intervalId = null;
            console.log("Geolocation tracking stopped.");
        }
    }

// Iniciar el tracking automáticamente cuando el framework web esté listo
// Esto se ejecutará cuando el cliente web principal de Odoo esté cargado.
// Considera si quieres iniciarlo siempre o bajo condiciones específicas.
    $(document).ready(function() {
        // Solo iniciar si el usuario está logueado (evita errores en página de login)
        if (session.user_id) {
            // Pequeña demora para asegurar que todo esté cargado
            setTimeout(startGeolocationTracking, 1000);
        }
    });

// Podrías exportar funciones si necesitas controlarlas desde otros módulos JS
    return {
        start: startGeolocationTracking,
        stop: stopGeolocationTracking,
    };

});