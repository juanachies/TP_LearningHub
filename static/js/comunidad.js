document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("formulario").addEventListener("submit", function(event) {
      let valid = true;
      const nombre = document.getElementById("nombre");
      const email = document.getElementById("email");
      const telefono = document.getElementById("telefono");
      const carrera = document.getElementById("carrera");
      const archivo = document.getElementById("archivo");
      const acepta = document.getElementById("acepta");
      const feedback = document.getElementById("feedback");
      
      feedback.innerHTML = ""; // Limpiar mensajes anteriores
      feedback.style.color = "red";

      if (nombre.value.trim() === "") {
        feedback.innerHTML += "⚠️ El nombre es obligatorio.<br>";
        valid = false;
      }

      const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
      if (!emailPattern.test(email.value.trim())) {
        feedback.innerHTML += "⚠️ Ingresá un correo válido.<br>";
        valid = false;
      }

      const telPattern = /^[0-9]{10}$/;
      if (!telPattern.test(telefono.value.trim())) {
        feedback.innerHTML += "⚠️ El teléfono debe tener 10 números sin espacios.<br>";
        valid = false;
      }

      if (carrera.value === "") {
        feedback.innerHTML += "⚠️ Seleccioná una carrera.<br>";
        valid = false;
      }

      if (!archivo.value || !archivo.value.toLowerCase().endsWith(".pdf")) {
        feedback.innerHTML += "⚠️ Solo se acepta un archivo PDF.<br>";
        valid = false;
      }

      if (!acepta.checked) {
        feedback.innerHTML += "⚠️ Tenés que aceptar compartir el material.<br>";
        valid = false;
      }

      if (!valid) {
        event.preventDefault(); // Evita que se envíe el formulario
        return false;
      } else {
        feedback.style.color = "green";
        feedback.innerHTML = "✅ ¡Formulario enviado con éxito!";
      }
    });
});