define(['jquery', 'base/js/utils', 'require'], function ($, utils, require) {

    // following variables define page elements

    // the page components
    var tab = '<li><a href="#nbmessage-board-admin" data-toggle="tab">UCSD ITS Messages (Admin)</a></li>';

    var tabContent = `
    <div id="nbmessage-board-admin" class="tab-pane container nbmessage-board">
        <div class="col-sm-2" id="nbmessage-nav"></div>
        <div class="col-sm-10" id="nbmessage-board-admin-content" style="padding-left: 1em"></div>
    </div>`

    class NavPills {
        constructor(appState) {
            this.form = `
            <ul class="nav nav-pills nav-stacked">
                <li role="presentation" id="nbmessage-tab-global" class="active"><a href="#">Global</a></li>
                <li role="presentation" id="nbmessage-tab-messages" ><a href="#">Messages</a></li>
            </ul>
            `

            this.render();
            this.appState = appState;
            $('[role="presentation"]').click(function() {
                var selectedTabname = $(this).text();
                appState.updateState({selectedTab: selectedTabname});
            });
        }

        render() {
            $('#nbmessage-nav').append(this.form);
        }

        removeActive() {
            $('#nbmessage-tab-global').removeClass('active');
            $('#nbmessage-tab-messages').removeClass('active');
        }

        addActive(tabname) {
            switch (tabname) {
                case 'Global':
                    $('#nbmessage-tab-global').addClass('active');
                    break;
                case 'Messages':
                    $('#nbmessage-tab-messages').addClass('active');
                    break;
            }
        }

        update(updatedState) {
            var selectedTab = updatedState.selectedTab;
            this.removeActive();
            this.addActive(selectedTab);
        }
    }

    class GlobalSubform {
        constructor(appState) {
            this.form = `
                <div id="nbmessage-global">
                    <h2 class="nbmessage-h2">Select a message board</h2>
                    <label for="select-message-board">Selected Message Board</label>
                    <select class="form-control" id="select-message-board" name="select_message_board"></select>
                </div>
            `

            this.appState = appState;

            this.render();

            $('#select-message-board').change(function() {
                appState.updateState({selectedMessageBoard: $(this).val()})
            });
        }

        render() {
            if ($('#nbmessage-global').length === 0) {
                var that = this;
                $('#nbmessage-board-admin-content').append(this.form);
                $.get(utils.get_body_data('baseUrl') + 'nbmessage/directories', function(data) {
                    var directories = JSON.parse(data);
                    directories.forEach(function(directory, i) {
                        if (i === 0) {
                            $('#select-message-board').append(`<option selected>${directory}</option>`);
                            that.appState.updateState({selectedMessageBoard: directory});
                        } else {
                            $('#select-message-board').append(`<option>${directory}</option>`);
                        }
                        
                    });
                });
            }
        }

        remove() {
            $('#nbmessage-global').remove();
        }

        update(updatedState) {
            if (updatedState.selectedTab === 'Global') {
                this.render();
            } else {
                this.remove();
            }
        }
    }

    class MessagesSubform {
        constructor(appState) {
            this.form = `
                <div class="form-group" id="nbmessage-operation-group">
                    <h2 class="nbmessage-h2">Select an operation to perform on course messages</h2>
                    <label for="message-operation">Message operation</label>
                    <select class="form-control" id="nbmessage-operation" name="message_operation">
                        <option>Add</option>
                        <option>Delete</option>
                    </select>
                </div>
            `

            this.addform = `
                <div class="nbmessage-form-group">
                    <form id="nbmessage-admin" method="post">
                        <div class="form-group" id="author">
                            <label for="author">Add your name to the message</label>
                            <input type="text" name="author" class="form-control" placeholder="Your name here" required>
                        </div>

                        <div class="form-group" id="message-id">
                            <label for="message-id">Add a message ID</label>
                            <input type="text" name="message_id" class="form-control" placeholder="message ID here" required>
                        </div>

                        <div class="form-group">
                            <label for="message-body">Add message body (note: must be formatted as a markdown document)</label>
                            <textarea class="form-control" rows="25" name="message_body" required></textarea>
                        </div>

                        <div class="form-check" id="set-notification">
                            <input type="checkbox" class="form-check-input"  name="setNotification">
                            <label class="form-check-label" for="setNotification">Add Notification</label>
                        </div>
                        <input name="status" type="hidden" value="preview">
                        <input name="operation" type="hidden" value="add">
                        <button type="submit" class="btn btn-default">Submit</button>
                    </form>

                    <div id="preview-modal" class="modal fade" role="dialog">
                        <div class="modal-dialog modal-lg" style="width:60em;">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                                    <h4 class="modal-title">Previewed Messages</h4>
                                    </div>
                                    <div class="modal-body"></div>
                                    <div class="modal-footer">
                                    <button type="button" id='save-message' class="btn btn-default" data-dismiss="modal">Save</button>
                                    <button type="button" id='close-modal' class="btn btn-default" data-dismiss="modal">Close</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div id="submit-modal" class="modal fade" role="dialog">
                        <div class="modal-dialog modal-lg" style="width:60em;">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                                    <h4 class="modal-title">Server Response</h4>
                                    </div>
                                    <div class="modal-body"></div>
                                    <div class="modal-footer">
                                    <button type="button" id='close-modal' class="btn btn-default" data-dismiss="modal">Close</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `

            this.deleteform = `
                <div class="nbmessage-form-group">
                    <div class="form-group" id="delete-message">
                        <label for="message-operation">Delete a message</label>
                        <select class="form-control" id="delete-message" name="delete-message"></select>
                    </div>
                </div>
            `

            this.selectedMessageBoard;
            this.messageOperation;
            this.appState = appState;

        }

        render() {
            if ($('#nbmessage-operation-group').length === 0) {
                $('#nbmessage-board-admin-content').append(this.form);
                this.showSubform(this.messageOperation);
                
                // event listeners are dependent on whether element exists in render step
                var that = this;
                $('#nbmessage-operation').change(function() {
                    that.appState.updateState({messageOperation: $(this).val()})
                });
            }
        }

        remove() {
            // empty?
            $('#nbmessage-operation-group').remove(); 
            $('.nbmessage-form-group').remove();
        }

        setupFormSubmit() {
            var that = this;
            $('#nbmessage-admin').off('submit');
            $('#nbmessage-admin').submit(function(event) {
                event.preventDefault();
                var form = $(this);
    
                // // pass data to app state
                var rawFormData = form.serializeArray();
                var formData = {};
                $(rawFormData).each(function(index, obj){
                    formData[obj.name] = obj.value;
                });
                
                // PREVIEW SUBMIT
                $.ajax({
                    type: form.attr('method'),
                    url: utils.get_body_data('baseUrl') + `nbmessage/messages/${that.selectedMessageBoard}`,
                    headers: {'X-CSRFToken': getCookie("_xsrf")},
                    data: JSON.stringify(formData)
                    // data: form.serialize()
                  }).done(function(template) {
                    // Optionally alert the user of success here...
                    $('.modal-body').empty();
                    $('.modal-body').append(template);
                    $('#preview-modal').modal('show');

                    // launch modal
                  }).fail(function(data) {
                    // Optionally alert the user of an error here...
                    console.log('failure');
                    console.log(data);
                });
                
                // SUBMITTED MESSAGE
                $('#save-message').click(function() {
                    formData.status = 'submit';
                    formData.operation = 'add';

                    $.ajax({
                        type: form.attr('method'),
                        url: utils.get_body_data('baseUrl') + `nbmessage/messages/${that.selectedMessageBoard}`,
                        headers: {'X-CSRFToken': getCookie("_xsrf")},
                        data: JSON.stringify(formData)
                      }).done(function(template) {
                        // Optionally alert the user of success here...
                        $('.modal-body').empty();
                        $('.modal-body').append(template);
                        $('#submit-modal').modal('show');
                        // launch modal
                      }).fail(function(data) {
                        // Optionally alert the user of an error here...
                        console.log('failure');
                        console.log(data);
                    });
                });
            });
    

        }

        showSubform(messageOperation) {
            // remove the existing subform and render selected one
            $('.nbmessage-form-group').remove();
    
            switch(messageOperation) {
                case 'Add':
                    $('#nbmessage-operation-group').after(this.addform);
                    this.setupFormSubmit();
                    break;

                case 'Delete':
                    $('#nbmessage-operation-group').after(this.deleteform);
                    $.get(utils.get_body_data('baseUrl') + `nbmessage/${this.selectedMessageBoard}/messages`, function(data) {
                        var messages = JSON.parse(data);
                        messages.forEach(function(message) {
                            $('#delete-message>select').append(`<option>${message}</option>`)
                        });
                    });
                    break;
            }
        }

        update(updatedState) {
            // update message board
            if (Object.keys(updatedState).indexOf('selectedMessageBoard') > -1) {
                this.selectedMessageBoard = updatedState.selectedMessageBoard;
            }

            // render the view or not
            if (updatedState.selectedTab === 'Messages') {
                this.render();
            } else {
                this.remove();
            }

            // operation selected
            this.messageOperation = updatedState.messageOperation;
            this.showSubform(this.messageOperation);
        }
    }

    class AppState {
        constructor() {
            this.state = {
                selectedMessageBoard: null,
                messageIdPreview: null,
                selectedTab: 'Global',
                messageOperation: 'Add'
            }

            this.stateListeners = []
        }  

        updateState(obj) {
            this.state = Object.assign(this.state, obj);
            var that = this;
            this.stateListeners.forEach(function(listener) {
                listener.update(that.state);
            });
        }

        registerStateListener(stateListener) {
            this.stateListeners.push(stateListener)
        }

    }

    function getCookie(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }

    var load_ipython_extension = function () {
        
        // Add Main Components
        $('#tabs').append(tab);
        $('.tab-content').append(tabContent);
        // $('#message-operation-group').after(addDomEl); 

        /** Class initializations */
        var appState = new AppState();

        var globalSubform = new GlobalSubform(appState);
        var navPills = new NavPills(appState);
        var messagesSubform = new MessagesSubform(appState);
        /**  Initialization data retrievals and updates */
        
        // setup the appState object, used as a command pattern to update state for all registered objects
        appState.registerStateListener(navPills);
        appState.registerStateListener(globalSubform);
        appState.registerStateListener(messagesSubform);

        // get the title
        $.get(utils.get_body_data('baseUrl') + 'nbmessage/admin', function(data) {
            var title = JSON.parse(data);
            $('#tab-title>input').attr("placeholder", title)
        });
        // todo add a spinner on click
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };
});
