$(document).ready(function() {
    // Update employee functionality
    $('#employeeTable').on('click', '.btn-update', function() {
        var employeeId = $(this).data('id');
        var row = $(this).closest('tr');

        // Populate the modal with employee data
        $('#employeeId').val(employeeId);
        $('#firstName').val(row.find('td').eq(0).text());
        $('#lastName').val(row.find('td').eq(1).text());
        $('#email').val(row.find('td').eq(2).text());
        $('#position').val(row.find('td').eq(3).text());
        $('#phoneNumber').val(row.find('td').eq(4).text());

        $('#updateEmployeeModal').modal('show');
    });

    // Handle form submission via AJAX for updating
    $('#updateEmployeeForm').on('submit', function(event) {
        event.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/update_employee/',
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (response.status === 'success') {
                    var employeeId = $('#employeeId').val();
                    var row = $('#employeeTable').find('tr[data-id="' + employeeId + '"]');

                    row.find('td').eq(0).text($('#firstName').val());
                    row.find('td').eq(1).text($('#lastName').val());
                    row.find('td').eq(2).text($('#email').val());
                    row.find('td').eq(3).text($('#position').val());
                    row.find('td').eq(4).text($('#phoneNumber').val());

                    $('#updateEmployeeModal').modal('hide');
                } else {
                    alert('An error occurred. Please try again.');
                }
            },
            error: function(xhr, status, error) {
                console.log('AJAX Error: ', status, error);
                alert('An error occurred. Please try again.');
            }
        });
    });

    // Delete employee functionality
    $('#employeeTable').on('click', '.btn-delete', function(event) {
        event.preventDefault();

        var employeeId = $(this).data('id');

        if (confirm('Are you sure you want to delete this employee?')) {
            $.ajax({
                type: 'POST',
                url: '/delete_employee/',
                data: {
                    'id': employeeId,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                headers: {
                    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    if (response.status === 'success') {
                        $('#employeeTable').find('tr[data-id="' + employeeId + '"]').remove();
                    } else {
                        alert('An error occurred. Please try again.');
                    }
                },
                error: function(xhr, status, error) {
                    console.log('AJAX Error: ', status, error);
                    alert('An error occurred. Please try again.');
                }
            });
        }
    });
});
