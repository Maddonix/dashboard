$(document).ready(function () {
    $("#centerDropdown, #productGroupDropdown").change(function () {
        console.log('Dropdown changed');
        var dropdownId = $(this).attr('id');
        var selectedId = $(this).val();
        var url = $(this).data('url');
        var cardBodyId = dropdownId == 'centerDropdown' ? '#centerCardBody' : '#productGroupCardBody';

        if (selectedId) {
            $.ajax({
                url: url,
                data: {
                    'id': selectedId
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data);  // print data to console for debugging
                
                    var parsedData = data // JSON.parse(data);  // parse the JSON string into a JavaScript object
                
                    if (parsedData.length < 1) {
                        console.error('No data returned from server');
                        return;
                    }
                
                    var fields = data // parsedData.fields;
                
                    if (!fields) {
                        console.error('No fields property in returned data');
                        return;
                    }
                
                    console.log(fields);
                
                    // Clear the card body
                    $(cardBodyId).empty();

                    // add pie chart using Plotly.js to card body; the field reference_product_material_tuples is a list of tuples
                    // where the first element is the material name and the second element is the material weight in grams
                    

                    
                
                    // Add each property to the card body
                    for (var key in fields) {
                        if (fields.hasOwnProperty(key)) {
                            console.log(key + " -> " + fields[key]);
                            $(cardBodyId).append("<p>" + key + ": " + fields[key] + "</p>");
                        }
                    }

                    var materialNames = [];
                    var materialWeights = [];

                    for (var i = 0; i < fields.reference_product_material_tuples.length; i++) {
                        materialNames.push(fields.reference_product_material_tuples[i][0]);
                        materialWeights.push(fields.reference_product_material_tuples[i][1]);
                    }

                    var data = [{
                        values: materialWeights,
                        labels: materialNames,
                        type: 'pie'
                    }];

                    var layout = {
                        title: 'Materials of Reference Product',
                        height: 400,
                        width: 500
                    };

                    $(cardBodyId).append('<div id="pieChart"></div>');
                    Plotly.newPlot('pieChart', data, layout);
                },
                
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error('Error during AJAX request:', textStatus, errorThrown);
                }
            });
        }
    });
});
