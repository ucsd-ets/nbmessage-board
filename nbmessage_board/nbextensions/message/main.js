define(['jquery', 'base/js/utils', 'require'], function ($, utils, require) {

    var tabContent = `
        <div id="nbmessage-board" class="tab-pane">
            <div class="container">
                <div class="row col-md-8 padding-bottom-sm main-border">

                    <h2>My message</h2>
                    <p style="padding-bottom: .5em;">Lorem ipsum dolor sit amet, accusamus tincidunt deterruisset vix ea, mea labores constituto no, at putant civibus vituperata eos. Sed ne dicat cotidieque ullamcorper. Ex qui blandit assueverit, suas vide munere ne per. Ancillae intellegam ut mea, sit cu tritani expetendis, id vis nibh omnis antiopam.

                    Sea at animal saperet, vix id erat habeo volumus. Eu admodum offendit recusabo cum, vim ad regione oporteat interpretaris. Ea eos option ceteros, alii verterem appellantur in nam. In enim consequat pro. Congue homero vituperata vix ut.
                    
                    No his doming maiorum suavitate, elit ocurreret referrentur qui at. Ei pro harum argumentum. Vim facer eleifend an. Ea eius adolescens pro, sea rebum exerci an. Ius sanctus eleifend ut, ad mel veri soleat, alia liber percipit cu quo.
                    
                    Has et consequat suscipiantur. Modus eripuit detracto cum eu. Homero mucius ea his. Sit te essent suscipit delicata, mea dicunt inciderint ad, meis audire alterum pro no.
                    
                    No erroribus rationibus mei, vel posse liber efficiendi ut, te cum mnesarchum moderatius omittantur. Vix no habeo nullam utamur, iisque definitionem his ne, duo ne quas cetero signiferumque. Wisi quas usu cu, his movet lobortis dissentias eu. Cu pro vitae labores. Mea ei hinc vide recusabo, at sit paulo tritani docendi, altera oblique est no.</p>
                
                    <div class="col-xs-4 nbmessage-background">
                        <div class="col-xs-12 user-fmt">
                            <p><i>12/1/2018 @ 1:00PM</i></p>
                        </div>
                        <div class="col-xs-2 nbmessage-thumbnail">
                            <img src="${utils.get_body_data('baseUrl') + 'nbmessage/images/ucsd-0.png'}" class="img-fluid img-thumbnail" alt="...">
                        </div>
                        <div class="col-xs-10">
                            <h4 class="user-fmt">Wesley Uykimpang</h4>
                        </div>
                    </div>            



                </div>

                <div class="row col-md-8">
                    <h1>Some update</h1>
                    <p>Yeah I know</p>
                </div>
            </div>
        </div>`

    var load_ipython_extension = function () {
        // add custom css
        $('head').append(`<link rel="stylesheet" type="text/css" href="${utils.get_body_data('baseUrl') + 'nbmessage/css/nbmessage-board.css'}">`)

        $.get(utils.get_body_data('baseUrl') + 'nbmessage/admin', function(data) {
            var title = JSON.parse(data);
            $('#tabs').append(`<li><a href="#nbmessage-board" data-toggle="tab">${title}</a></li>`)
            $('.tab-content').append(tabContent);
        });
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };
});
