$(document).ready(function () {

    // Get array of used modules
    const modules = JSON.parse($("#modules").text().replace(/'/g, '"'));

    // Set width for module column in table
    var character_count = modules.map(x => x.length).reduce((accum, current_val) => Math.max(accum, current_val), $("#known_correct_module").text().length);
    $("#module_column").css("width", `${character_count * 10}px`);

    // Get array of the currently correct words (can be multiple, i.e. brother/brethren)
    var currently_correct = [];

    var show_competitors = false;

    // sending a connect request to the server.
    var socket = io.connect('http://localhost:5000');

    // Emit the request for output given the current inputs
    function emit_input() {
        // Set form validation
        var form = $('#inflex_form')[0];
        form.classList.add('was-validated');
        if (!form.checkValidity()) {
            return;
        }

        socket.emit("input", {
            pos: $("#pos").val(),
            wordform: $("#wordform").val(),
            word: $("#word").val(),
            show_competitors: show_competitors,
        });

        clear_all_outputs();
    }

    // Emit the request for which modules should be shown
    function emit_input_modules() {
        socket.emit("input_modules", {
            pos: $("#pos").val(),
            wordform: $("#wordform").val(),
            show_competitors: show_competitors
        });
    }

    // Apply is-valid or is-invalid class based on value as compared to currently_correct
    function validate(output) {
        if (currently_correct.length) {
            var value = output.val()
            if (value) {
                if (currently_correct.includes(value)) {
                    output.addClass("is-valid");
                }
                else {
                    output.addClass("is-invalid");
                }
            }
        }
    }

    // Disable Past, Past Participle and Present Participle if a POS other than Verb is selected
    function toggle_wordform_disabled(pos) {
        const all_wordforms = ["sing", "plur", "past", "past_part", "pres_part", "comp", "super"];
        const wordforms = {
            "v": ["sing", "plur", "past", "past_part", "pres_part"],
            "n": ["sing", "plur"],
            "a": ["sing", "plur", "comp", "super"],
        };
        all_wordforms.forEach(word_form => {
            if (wordforms[pos].includes(word_form)){
                $(`#wordform option[value='${word_form}']`).prop('disabled', false);
            }
            else{
                $(`#wordform option[value='${word_form}']`).prop('disabled', true);
            }
        });
        // If one of the wordforms that will be disabled has been selected, reset to the first legal option
        var wordform_selector = $('#wordform')[0];
        if (!wordforms[pos].includes(wordform_selector.value)) {
            wordform_selector.value = wordforms[pos][0];
        }
    }

    // Show the Known Correct row, but only if all visible outputs are incorrect.
    function opt_show_correct() {
        if (currently_correct.length) {
            // Return if there exists a visible row with no output, 
            // or if there is a visible row that is correct
            for (i = 0; i < modules.length; i++) {
                var module = modules[i];
                var row = $(`#${module}_row`);
                if (row.is(":visible")) {
                    var output = $(`#${module}_output`);
                    if (output.hasClass("is-valid") || output.val().length == 0) {
                        return;
                    }
                }
            }

            // Otherwise, show known correct
            $("#known_correct_row").show();
        }
    }

    // Straight away find which modules can be used
    emit_input_modules();

    // Reset all formatting classes from this output
    function reset_output_classes(output) {
        output.removeClass("italic");
        output.removeClass("is-invalid");
        output.removeClass("is-valid");
        output.removeClass("is-warning");
    }

    // Clear the output field for all modules, including italic and colors
    function clear_all_outputs() {
        currently_correct = [];
        $("#known_correct_output").val("");
        reset_output_classes($("#known_correct_output"));
        $("#known_correct_row").hide();

        modules.forEach(module => {
            var output = $(`#${module}_output`);
            output.val("");
            reset_output_classes(output);
        });
    }

    // Update which Wordform options are allowed, given the current POS,
    // also find out which modules should be shown given the current POS and Wordform
    $('#pos').change(function () {
        toggle_wordform_disabled(this.value);

        // Emit the request for which modules should be shown
        emit_input_modules();
    });

    // Find out which modules should be shown given the current POS and Wordform
    $('#wordform').change(function () {
        // Emit the request for which modules should be shown
        emit_input_modules();
    });

    // Override show competitors button click to request new input modules
    $('#competitors_button').unbind("click").bind("click", function () {
        show_competitors = !show_competitors;
        $('#competitors_button').text(show_competitors ? "Hide Competitors" : "Show Competitors");
        emit_input_modules();

        // If we are now going to show competitors, and we already have a word filled out, then do Go
        if ($("#word")[0].value) {
            emit_input();
        }
    });

    // Override Random button click to send "Random" request to Server
    $('#random').unbind("click").bind("click", function () {
        socket.emit("random", {
            show_competitors: show_competitors
        });
    });

    // After successfully connecting to the Server
    socket.on('after connect', function (msg) {
        console.log('Successfully connected to server.');
    });

    // Getting input parameters from the random choice from the Server
    socket.on('conversion', function (json) {
        $('#pos').val(json["pos"]);
        toggle_wordform_disabled(json["pos"]);
        $('#wordform')[0].value = json["wordform"];
        $('#word').val(json["word"]);
        // Set was-validated to give the inputs color
        var form = $('#inflex_form')[0];
        form.classList.add('was-validated');
    });

    // Getting outputs from the Server
    socket.on('output', function (json) {
        // console.log("Received output: ");
        // console.log(json);
        var output = $(`#${json['module']}_output`);
        if (json["output"]) {
            reset_output_classes(output);
            output.val(json["output"]);
            validate(output);
        }
        else {
            output.addClass("italic");
            output.addClass("is-warning");
            output.val("Output was an empty string.");
        }

        // Optionally show known correct table row
        opt_show_correct();
    });

    // Getting the known correct output from the Server
    socket.on('correct', function (json) {
        var output = $(`#known_correct_output`);
        currently_correct = json["output"];

        output.addClass("is-valid");
        output.val(currently_correct.join(", "));

        // Set is-valid or is-invalid on already filled in outputs
        modules.forEach(module => {
            var output = $(`#${module}_output`);
            validate(output);
        });

        // Optionally show known correct table row
        opt_show_correct();
    });

    // Getting which modules should be visible from the Server
    socket.on('output_modules', function (json) {
        clear_all_outputs();
        modules.forEach(module => {
            if (json["modules"].includes(module)) {
                $(`#${module}_row`).show();
            }
            else {
                $(`#${module}_row`).hide();
            }
        });
    });

    // Override Submit and send the inputs to the Server
    $('#inflex_form').submit(function (e) {
        e.preventDefault();
        emit_input();
    });
});