define(['jquery', 'base/js/utils', 'require'], function ($, utils, require) {

    var tab = '<li><a href="#nbmessage-board-admin" data-toggle="tab">UCSD ITS Messages (Admin)</a></li>';
    var tabContent = `
    <div id="nbmessage-board-admin" class="tab-pane container">

        <div class="row col-sm-10" >
            
            <form class="needs-validation" action="/admin" method="post" id="nbmessage-admin">
                <h2>Global Functions</h2>
                <div id="global-functions">
                    <div class="form-group">
                        <label for="publish-mode">Publish Mode</label>
                        <select class="form-control" id="publish-mode" name="publishMode">
                            <option>Staging</option>
                            <option>Publish</option>
                        </select>
                    </div>

                    <div class="form-group" id="tab-title">
                        <label for="setTabTitle">Set the tab title</label>
                        <input type="text" name="tabTitle" class="form-control" placeholder="UCSD ITS Messages">
                        <div class="invalid-feedback">
                            Please choose a username.
                        </div>
                    </div>  
                </div>

                <h2>Manage Messages</h2>
                <div class="form-group" id="message-operation-group">
                    <label for="message-operation">Message operation</label>
                    <select class="form-control" id="message-operation" name="messageOperation">
                        <option>Add</option>
                        <option>Delete</option>
                        <option>None</option>
                    </select>
                </div>
        
                <button type="submit" class="btn btn-primary" name="admin">Submit</button>
            </form>
        </div>
    </div>`

    var addDomEl = `
    <div id="add-form-group">
        <div class="form-group" id="newMessageFilePath">
            <label for="newMessageFilePath">New Message File Path</label>
            <input type="text" name="newMessageFilePath" class="form-control" placeholder="some path here to .md file..." required>
        </div>
        
        <div class="form-check" id="set-notification">
            <input type="checkbox" class="form-check-input"  name="setNotification">
            <label class="form-check-label" for="setNotification">Add Notification</label>
        </div>   
    </div>
    `
    var deleteDomEl = `
    <div class="form-group" id="delete-message">
        <label for="message-operation">Delete a message</label>
        <select class="form-control" id="delete-message" name="delete-message">
        </select>
    </div>
    `

    function getCookie(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }

    var load_ipython_extension = function () {
        $('#tabs').append(tab);
        $('.tab-content').append(tabContent);
        $('#message-operation-group').after(addDomEl);

        // add tab setting, update it's contents
        $.get(utils.get_body_data('baseUrl') + 'nbmessage/admin', function(data) {
            var title = JSON.parse(data);
            $('#tab-title>input').attr("placeholder", title)
        });

        // submit button for form
        $('#nbmessage-admin').submit(function(event) {
            event.preventDefault();
            var form = $(this);

            $.ajax({
                type: form.attr('method'),
                url: utils.get_body_data('baseUrl') + 'nbmessage/admin',
                headers: {'X-CSRFToken': getCookie("_xsrf")},
                data: form.serialize()
              }).done(function(data) {
                // Optionally alert the user of success here...
                
                var message = data;
                if (message.hasOwnProperty('error')) {
                    var componentId = message.error;
                    var message = message.message;
                    $(`#${componentId}`).addClass('has-error')
                                        .append(`<div id="error"><p class="text-danger">${message}</p></div>`)

                }

                // launch modal
              }).fail(function(data) {
                // Optionally alert the user of an error here...
                console.log('failure');
                console.log(data);
              });
        });

        // subform handler for adding/remove
        $('#message-operation').change(function() {
            var operation = $(this).val();

            switch (operation) {
                case 'Add':
                    if ($('#delete-message').length !== 0) {
                        $('#delete-message').remove();
                    }  

                    if ($('#add-form-group').length === 0) {
                        $('#message-operation-group').after(addDomEl);
                    }
                    break;
                case 'Delete':
                    if ($('#add-form-group').length !== 0) {
                        $('#add-form-group').remove();
                    }  
                    if ($('#delete-message').length === 0) {
                        $('#message-operation-group').after(deleteDomEl);
                        // fill the delete message form element with options
                        $.get(utils.get_body_data('baseUrl') + 'nbmessage/messages', function(data) {
                            var messages = JSON.parse(data);
                            messages.forEach(function(message) {
                                $('#delete-message>select').append(`<option>${message}</option>`)
                            });
                        });
                    }
                    break;
                case 'None':
                    $('#add-form-group').remove();
                    $('#delete-message').remove();
                    break;
                    
            }
            
        });

        // todo add a spinner on click
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };
});
