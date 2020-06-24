define(['jquery', 'base/js/utils', 'require'], function ($, utils, require) {
    var tabContent = `
    <div id="nbmessage-board" class="tab-pane nbmessage-board">
        <div class="col-sm-2">
            <ul class="nav nav-pills nav-stacked" id="nbmessage-boards"></ul>
        </div>
        <div class="col-sm-10" id="nbmessage-messages"></div>
    </div>`
    // var tabContent = `
    //     <div id="nbmessage-board" class="tab-pane">
    //         <div class="container col-md-offset-2">
    //             <div class="row col-md-8 padding-bottom-sm main-border">

    //                 <h2>My message</h2>
    //                 <p style="padding-bottom: .5em;">Lorem ipsum dolor sit amet, accusamus tincidunt deterruisset vix ea, mea labores constituto no, at putant civibus vituperata eos. Sed ne dicat cotidieque ullamcorper. Ex qui blandit assueverit, suas vide munere ne per. Ancillae intellegam ut mea, sit cu tritani expetendis, id vis nibh omnis antiopam.

    //                 Sea at animal saperet, vix id erat habeo volumus. Eu admodum offendit recusabo cum, vim ad regione oporteat interpretaris. Ea eos option ceteros, alii verterem appellantur in nam. In enim consequat pro. Congue homero vituperata vix ut.
                    
    //                 No his doming maiorum suavitate, elit ocurreret referrentur qui at. Ei pro harum argumentum. Vim facer eleifend an. Ea eius adolescens pro, sea rebum exerci an. Ius sanctus eleifend ut, ad mel veri soleat, alia liber percipit cu quo.
                    
    //                 Has et consequat suscipiantur. Modus eripuit detracto cum eu. Homero mucius ea his. Sit te essent suscipit delicata, mea dicunt inciderint ad, meis audire alterum pro no.
                    
    //                 No erroribus rationibus mei, vel posse liber efficiendi ut, te cum mnesarchum moderatius omittantur. Vix no habeo nullam utamur, iisque definitionem his ne, duo ne quas cetero signiferumque. Wisi quas usu cu, his movet lobortis dissentias eu. Cu pro vitae labores. Mea ei hinc vide recusabo, at sit paulo tritani docendi, altera oblique est no.</p>
                
    //                 <div class="col-xs-4 nbmessage-background">
    //                     <div class="col-xs-12 user-fmt">
    //                         <p><i>12/1/2018 @ 1:00PM</i></p>
    //                     </div>
    //                     <div class="col-xs-2 nbmessage-thumbnail">
    //                         <img src="${utils.get_body_data('baseUrl') + 'nbmessage/images/ucsd-0.png'}" class="img-fluid img-thumbnail" alt="...">
    //                     </div>
    //                     <div class="col-xs-10" style="padding-top: .3em">
    //                         <h4 class="user-fmt">Wesley Uykimpang</h4>
    //                     </div>
    //                 </div>            

    //             </div>

    //             <div class="row col-md-8 padding-bottom-sm main-border">

    //                 <h2>My message</h2>
    //                 <p style="padding-bottom: .5em;">Lorem ipsum dolor sit amet, accusamus tincidunt deterruisset vix ea, mea labores constituto no, at putant civibus vituperata eos. Sed ne dicat cotidieque ullamcorper. Ex qui blandit assueverit, suas vide munere ne per. Ancillae intellegam ut mea, sit cu tritani expetendis, id vis nibh omnis antiopam.

    //                 Sea at animal saperet, vix id erat habeo volumus. Eu admodum offendit recusabo cum, vim ad regione oporteat interpretaris. Ea eos option ceteros, alii verterem appellantur in nam. In enim consequat pro. Congue homero vituperata vix ut.
                    
    //                 No his doming maiorum suavitate, elit ocurreret referrentur qui at. Ei pro harum argumentum. Vim facer eleifend an. Ea eius adolescens pro, sea rebum exerci an. Ius sanctus eleifend ut, ad mel veri soleat, alia liber percipit cu quo.
                    
    //                 Has et consequat suscipiantur. Modus eripuit detracto cum eu. Homero mucius ea his. Sit te essent suscipit delicata, mea dicunt inciderint ad, meis audire alterum pro no.
                    
    //                 No erroribus rationibus mei, vel posse liber efficiendi ut, te cum mnesarchum moderatius omittantur. Vix no habeo nullam utamur, iisque definitionem his ne, duo ne quas cetero signiferumque. Wisi quas usu cu, his movet lobortis dissentias eu. Cu pro vitae labores. Mea ei hinc vide recusabo, at sit paulo tritani docendi, altera oblique est no.</p>
                
    //                 <div class="col-xs-4 nbmessage-background">
    //                     <div class="col-xs-12 user-fmt">
    //                         <p><i>12/1/2018 @ 1:00PM</i></p>
    //                     </div>
    //                     <div class="col-xs-2 nbmessage-thumbnail">
    //                         <img src="${utils.get_body_data('baseUrl') + 'nbmessage/images/ucsd-0.png'}" class="img-fluid img-thumbnail" alt="...">
    //                     </div>
    //                     <div class="col-xs-10" style="padding-top: .3em">
    //                         <h4 class="user-fmt">Wesley Uykimpang</h4>
    //                     </div>
    //                 </div>            
                    
    //             </div>
    //         </div>
    //     </div>`

    class MessageBoardsPill {
        constructor(appState) {
            $.get(utils.get_body_data('baseUrl') + 'nbmessage/directories', function(data) {
                var directories = JSON.parse(data);
                directories.forEach(function(directory, index) {
                    if (index === 0) {
                        $('#nbmessage-boards').append(`<li role="presentation" class="active"><a href="#">${directory}</a></li>`)
                        appState.updateState({selectedMessageBoard: directory});
                    } else {
                        $('#nbmessage-boards').append(`<li role="presentation" class="nbmessage-pill"><a href="#">${directory}</a></li>`)
                    }
                });
            
                $('.nbmessage-pill').click(function() {
                    var selectedTabname = $(this).text();
                    appState.updateState({selectedMessageboard: selectedTabname});
                    that.removeActive();
                    $(this).addClass('active');
                });

            });

            this.appState = appState;
            var that = this;


        }

        removeActive() {
            $('.nbmessage-pill').removeClass('active');
        }

    }

    class Messages {
        constructor() {
            this.messagesHTML = undefined;
        }

        update(obj) {
            var messageBoard = obj.selectedMessageBoard;
            var that = this;

            $.get(utils.get_body_data('baseUrl') + 'nbmessage/render/' + messageBoard, function(data) {
                data = JSON.parse(data);
                
                // only update the html if it doesnt exist
                if (!that.messagesHTML) {
                    that.messagesHTML = data.html;
                    $('#nbmessage-messages').append(that.messagesHTML);
                }
            }).fail(function() { });
        }

    }

    class MessageState {
        constructor() {
            this.state = {
                selectedMessageBoard: null
            }
            this.stateListeners = [];
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


    var load_ipython_extension = function () {
        // add custom css
        $('head').append(`<link rel="stylesheet" type="text/css" href="${utils.get_body_data('baseUrl') + 'nbmessage/css/nbmessage-board.css'}">`);
        
        // set the tab title, everything must take place once the tab is established
        $.get(utils.get_body_data('baseUrl') + 'nbmessage/admin', function(data) {
            var messageState = new MessageState();
            var title = JSON.parse(data);
            $('#tabs').append(`<li><a href="#nbmessage-board" id="nbmessage-board-tab" data-toggle="tab">${title}</a></li>`)
            $('.tab-content').append(tabContent);

            // set listener on tab
            $('#nbmessage-board-tab').click(function() {
                messageState.updateState({'clicked': true});
            });
            var messageBoardPill = new MessageBoardsPill(messageState);
            var messages = new Messages();
    
            messageState.registerStateListener(messages);

        });




    };

    return {
        load_ipython_extension: load_ipython_extension,
    };
});
