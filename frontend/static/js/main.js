(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();

    // Initiate the wowjs
    new WOW().init();

    // Fixed Navbar
    $('.fixed-top').css('top', $('.top-bar').height());
    $(window).scroll(function () {
        if ($(this).scrollTop()) {
            $('.fixed-top').addClass('bg-dark').css('top', 0);
        } else {
            $('.fixed-top').removeClass('bg-dark').css('top', $('.top-bar').height());
        }
    });

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });

    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: false,
        smartSpeed: 1500,
        loop: true,
        nav: true,
        dots: false,
        items: 1,
        navText: [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });

 
    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: false,
        smartSpeed: 1000,
        margin: 25,
        loop: true,
        center: true,
        dots: false,
        nav: true,
        navText: [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            }
        }
    });

    // Funcionalidad de carrito de compras
    var cart = []; // Array para almacenar los productos en el carrito

    // Función para agregar un producto al carrito
    function addToCart(productId) {
        // Obtener el producto por su ID (aquí puedes implementar tu lógica específica)
        var product = getProductById(productId);
        if (product) {
            cart.push(product); // Agregar el producto al carrito
            updateCart(); // Actualizar la interfaz de usuario del carrito
        }
    }

    // Función para actualizar la interfaz de usuario del carrito
    function updateCart() {
        console.log("Carrito actualizado:", cart);
        // Aquí puedes implementar la lógica para mostrar los productos en el carrito
    }

    // Función para obtener un producto por su ID (aquí puedes implementar tu lógica específica)
    function getProductById(productId) {
        // Por simplicidad, aquí simplemente devolveremos un objeto de ejemplo
        var products = [
            { id: 1, name: "Muffin", price: 1200 },
            { id: 2, name: "Pan", price: 1300 },
            { id: 3, name: "Galletitas", price: 1800 }
        ];
        return products.find(function (product) { return product.id === productId; });
    }

    // Mostrar u ocultar el resumen de la compra al hacer clic en el botón del carrito
    $('#cart-button').click(function () {
        $('#cart-summary').toggleClass('show');
    });


// Mostrar u ocultar el resumen de la compra al hacer clic en el botón del carrito
$('.new-minicart-button').click(function () {
    $('#cart-summary').toggleClass('show');
});

})(jQuery);
