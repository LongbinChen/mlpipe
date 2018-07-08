// TODO add method of renaming labels
// TODO make dropdown including filenames
// TODO make dropdown including types of accepted data inputs
// TODO determine json scheme or convert directly to pipe

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var idNum = 0;
var nodes = {};

jsPlumb.ready(function () {

    var instance = window.jsp = jsPlumb.getInstance({
        // default drag options
        DragOptions: { cursor: 'pointer', zIndex: 2000 },
        // the overlays to decorate each connection with.  note that the label overlay uses a function to generate the label text; in this
        // case it returns the 'labelText' member that we set on each connection in the 'init' method below.
        ConnectionOverlays: [
            [ "Arrow", {
                location: 1,
                visible:true,
                width:11,
                length:11,
                id:"ARROW",
                events:{
                    click:function() { alert("you clicked on the arrow overlay") }
                }
            } ],
            [ "Label", {
                location: 0.1,
                id: "label",
                cssClass: "aLabel",
                events:{
                    tap:function() { alert("hey"); }
                }
            }]
        ],
        Container: "canvas"
    });

    var basicType = {
        connector: "StateMachine",
        paintStyle: { stroke: "red", strokeWidth: 4 },
        hoverPaintStyle: { stroke: "blue" },
        overlays: [
            "Arrow"
        ]
    };
    instance.registerConnectionType("basic", basicType);

    instance.batch(function () {

        // listen for new connections; initialise them the same way we initialise the connections at startup.
        instance.bind("connection", function (connInfo, originalEvent) {
            init(connInfo.connection);
        });

        // make all the window divs draggable
        instance.draggable(document.querySelectorAll(".flowchart-demo .window"), { grid: [20, 20] });
        // THIS DEMO ONLY USES getSelector FOR CONVENIENCE. Use your library's appropriate selector
        // method, or document.querySelectorAll:
        //jsPlumb.draggable(document.querySelectorAll(".window"), { grid: [20, 20] });

        // listen for clicks on connections
        instance.bind("click", function (conn, originalEvent) {
            conn.toggleType("basic");
        });

        instance.bind("dblclick", function (conn, originalEvent) {
            instance.detach(conn);
        });

        instance.bind("contextmenu", function (node, port, el, e) {

        });

        instance.bind("connectionDrag", function (connection) {
            console.log("connection " + connection.id + " is being dragged. suspendedElement is ", connection.suspendedElement, " of type ", connection.suspendedElementType);
        });

        instance.bind("connectionDragStop", function (connection) {
            console.log("connection " + connection.id + " was dragged");
        });

        // TODO change id so that includes path
        $(document).draggable();
        $(document).on('click', '.window', function () {
            var modPath = this.getAttribute("file");
            var nodeId = this.getAttribute("id");
            var data = {filename: modPath, id: nodeId, params: nodes[nodeId].params};
            $.post("/openmodal", JSON.stringify(data), function (response) {
                jQuery.noConflict();
                document.getElementById("param-info").innerHTML = response;
                var windowHeight = $(window).height();
                var windowWidth = $(window).width();
                var boxHeight = $('#modal'+nodeId).height();
                var boxWidth = $('#modal'+nodeId).width();
                $('#modal'+nodeId).modal('show').css({
                    'left': ((windowWidth - boxWidth)/2),
                    'top': ((windowHeight - boxHeight)/2)
                });
                $("[id$='type']").change(function () {
                    var id = this.id.slice(0, -4);
                    var option = $("#"+id+"type option:selected").val();
                    switch (option) {
                        case "file":
                            // can use jstree to display a file viewer
                            $("#"+id+"input"+option).css({
                                "display": "block"
                            });
                            break;
                        case "s3":
                            $("#"+id+"input"+option).css({
                                "display": "block"
                            });
                            break;
                        case "http":
                            $("#"+id+"input"+option).css({
                                "display": "block"
                            });
                            break;
                        default:
                            console.log(option + " is not supported");
                            break;
                    }
                }).change();
                /*
                if (nodes[nodeId]["params"] == {}) {
                    // TODO loop through params in response and add relevant to nodes object
                    nodes[nodeId]["param"][param] = {}
                }*/
                var submit = document.getElementById("param-save")
                submit.addEventListener("click", function () {
                    // TODO add cleanup
                    var form = document.getElementById("modal"+nodeId);
                    var params = form.getElementsByTagName("input");
                    var defaults = form.getElementsByTagName("p");
                    var defaultOffset = 0;
                    console.log(params)
                    for (var i = 0; i < params.length; i++) {
                        var paramVal = params[i].getAttribute("value");
                        var paramName = params[i].getAttribute("id");
                        var paramType = "param";
                        if (params[i].getAttribute("type") == "file" || params[i].getAttribute("type") == "url") {
                            paramType = "input";
                            defaultOffset += 1;
                            if (paramName.endsWith("output")) {
                                paramType = "output";
                            }
                            if (!nodes[nodeId][paramType]) {
                                nodes[nodeId][paramType] = {}
                            }
                            if (!nodes[nodeId][paramType][paramName]) {
                                nodes[nodeId][paramType][paramName] = {}
                            }
                            nodes[nodeId][paramType][paramName].current = paramVal;
                        } else if (params[i].getAttribute("type") != "hidden") {
                            console.log(i-defaultOffset);
                            var paramDefault = defaults[i-defaultOffset].innerHTML.slice(9);
                            if (!nodes[nodeId]["param"]) {
                                nodes[nodeId]["param"] = {}
                            }
                            if (!nodes[nodeId]["param"][paramName]) {
                                nodes[nodeId]["param"][paramName] = {}
                            }
                            nodes[nodeId][paramType][paramName].defaultVal = paramDefault;
                            nodes[nodeId][paramType][paramName].current = paramVal;
                        } else {
                            defaultOffset += 1;
                        }
                    }
                });
            });
        });

        $(document).on('dblclick', '.window', function () {
            instance.remove($(this));
        });
    });

    jsPlumb.fire("jsPlumbDemoLoaded", instance);

});
