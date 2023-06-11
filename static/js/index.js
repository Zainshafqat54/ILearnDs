const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
const pages = document.querySelectorAll(".page");
    const translateAmount = 100; 
    let translate = 0;

    slide = (direction) => {

      direction === "next" ? translate -= translateAmount : translate += translateAmount;

      pages.forEach(
        pages => (pages.style.transform = `translateX(${translate}%)`)
      );
    }

(function () {
   window.supportDrag = (function () {
      let div = document.createElement("div");
      return (
         ("draggable" in div || ("ondragstart" in div && "ondrop" in div)) &&
         "FormData" in window &&
         "FileReader" in window
      );
   })();

   let input = document.getElementById("js-file-input");

   if (!supportDrag) {
      document.querySelectorAll(".has-drag")[0].classList.remove("has-drag");
   }

   input.addEventListener(
      "change",
      function (e) {
         document.getElementById("js-file-name").innerHTML = this.files[0].name;
         document.querySelector('.Proceed_btn').disabled = false;
      },
      false
   );

   if (supportDrag) {
      input.addEventListener("dragenter", function (e) {
         document
            .querySelectorAll(".file-input")[0]
            .classList.add("file-input--active");
      });

      input.addEventListener("dragleave", function (e) {
         document
            .querySelectorAll(".file-input")[0]
            .classList.remove("file-input--active");
      });
   }
})();

$('input[type="file"]').on('change', function () {
    var reader = new FileReader();
    reader.onload = function () {
        var thisImage = reader.result;
        localStorage.setItem("imgData", thisImage);
    };
    reader.readAsDataURL(this.files[0]);
});

// $(".Proceed_btn").click(function()
// {
// //    $.post('/upload', function(response) {
// //   // Do something with the response from the Flask app
// //   alert("hello");
// // });
//    $('#fileUploadingForm').submit();
// });