// public/app.js

$(document).ready(function () {
    // Handle PDF Upload
    $("#uploadBtn").click(function () {
        let file = $("#pdfFile")[0].files[0];
        if (!file) {
            alert("Please select a PDF file.");
            return;
        }

        let formData = new FormData();
        formData.append("file", file);

        $.ajax({
            url: "/upload",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $("#uploadStatus").text(response.message);
            },
            error: function () {
                $("#uploadStatus").text("Error uploading file.");
            }
        });
    });

    // Handle Question Asking
    $("#askBtn").click(function () {
        let question = $("#question").val();
        if (!question) {
            alert("Please enter a question.");
            return;
        }

        $.ajax({
            url: "/ask",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ question: question }),
            success: function (response) {
                $("#chatBox").append(`<p><b>You:</b> ${question}</p>`);
                $("#chatBox").append(`<p><b>Bot:</b> ${response.answer}</p>`);
                $("#question").val("");
            },
            error: function () {
                $("#chatBox").append(`<p><b>Bot:</b> Error getting answer.</p>`);
            }
        });
    });
});
