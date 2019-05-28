var t;
var reg = new RegExp(['«?(0?[1-9]|[1-2]\\d|3[01])»?(\\.|\\/|\\s|-)', // День + разделяющий символ (. / - пробел)
        '(1[012]|0?[1-9]|([яЯ]нв(\\.|аря|арь)?)|([фФ]евр(\\.|аля|аль)?)|',
        '([мМ]ар(\\.|та|т)?)|([аА]пр(\\.|еля|ель)?)|([мМ]а[йя])|',
        '([иИ]юн[яь])|([иИ]юл[ья])|([аА]вг(\\.|уста|уста)?)|',
        '([сС]ент(\\.|ябрь|ября)?)|([оО]кт(\\.|ября|ябрь)?)|([нН]ояб(\\.|ря|рь)?)|',
        '([дД]ек(\\.|абря|абрь)?))', // Месяц - либо число, либо название, либо сокращенное название
        '\\2((20)?[01]\\d)'].join(''), 'g'); // разделяющий символ, такой же как в первый раз + год 2000-2019, может быть без первых двух цифр
var dates = []

$(document).ready(function() {
    if (document.getElementById('cur_name').innerHTML != 'Документ не загружен') {
        time = localStorage.getItem('timer');
        if (time){
            $('#h4c').css("visibility", "visible");
            $('#my_timer').text(time);
            startTimer();
        }
    }
});

$(document).ready(function() {
    $('#form_params').on("submit", function(event) {
        var dataObj = $('#form_params').serializeArray();
        arr = [];
        $(".add_label").each(function() {
            arr.push({"name" : $(this).attr("id"), "value" : $(this).text()});
        });
        dataObj = dataObj.concat(arr.reverse());
        $.ajax({
            data: dataObj,
            type : 'POST',
            url : '/get_params'
        }).done(function(response) {
            alert(response['status']);
            get_next('#cur_txt', '#cur_name');
        }).fail(function() {
            alert('Что-то пошло не так(');
        });
        event.preventDefault();
        $.each(dataObj, function(i, data) {
            $('#' + data.name).val('');
            $('#' + data.name + '_pos').text('');
            $('#' + data.name + '_cb').prop('checked', false);
        });
    });
});

function dateHighliting(text) {
    function replacer(match) {
        dates.push(text.indexOf(match));
        dates.push(text.indexOf(match) + match.length);
        return '<span style="background-color: yellow;">' + match + '</span>';
    }
    return text.replace(reg, replacer);
}

function undoHighliting(text) {
    text = text.replace('<span style="background-color: yellow;">', '');
    return text.replace('</span>', '');
}

function get_next(txt, name) {
    $.get('/next_doc').done(function(response) {
        if (t != undefined) {
            clearTimeout(t);
        }
        if (response['pdf'] != '') {
            $("#containerPDF").children().each(function() {$(this).remove()});
            getDoc(response['pdf']);
            $(name).text(response['name']);
            $('#my_timer').text("00:10:00");
            $('#h4c').css("visibility", "visible");
            dates = [];
            startTimer();
        } else {
            $("#containerPDF").children().each(function() {$(this).remove()});
            $(name).text(response['name']);
            $(txt).text('');
            $('#hidden_text').html('');
            $('#submit').prop('disabled', true);
            $('#h4c').css("visibility", "hidden");
            dates = [];
        }
    }).fail(function() {
        alert("Что-то пошло не так(");
    });
}

function getSel(x, pos) {
    $('#cur_txt').off( "select" );
    $('#cur_txt').off( "click" );
    $("#containerPDF").off("mouseup")
    $('.textLayer').children().each(function() {
        $(this).html(undoHighliting($(this).html()));
    });
    $('#hidden_text').html('');
    $("#containerPDF").mouseup(function() {
        sel = window.getSelection().toString();
        start = document.getElementById("cur_txt").innerHTML.indexOf(sel);
        finish = start + sel.length;
        $(x).val(sel);
        if ((start != finish) && ($(x).val() != '')) {
            $(pos).text('От ' + start + ' до ' + finish);
        }
        $('#containerPDF').off( "mouseup" );
        $('#cur_txt').off( "select" );
    });
    $('#cur_txt').select(function () {
        var start = this.selectionStart;
        var finish = this.selectionEnd;$(this).attr("type")
        var sel = this.value.substring(start, finish);
        $(x).val(sel);
        if ((start != finish) && ($(x).val() != '')) {
            $(pos).text('От ' + start + ' до ' + finish);
        }
        this.setSelectionRange(start, start);
        $('#cur_txt').off( "select" );
    });
}

function getSel1(x, pos) {
    $('.textLayer').children().each(function() {
        $(this).html(dateHighliting($(this).html()));
    });
    $('#hidden_text').html(dateHighliting(document.getElementById("cur_txt").innerHTML));
    $('#cur_txt').off( "click" );
    $("#containerPDF").off("mouseup")
    $("#containerPDF").mouseup(function() {
        alert(p.pageX, p.pageY);
        sel = window.getSelection().toString();
        start = $("#cur_txt").text().indexOf(sel);
        finish = start + sel.length;
        $(x).val(sel);
        if ((start != finish) && ($(x).val() != '')) {
            $(pos).text('От ' + start + ' до ' + finish);
        }
        $('#containerPDF').off( "mouseup" );
        $('#hidden_text').html('');
        $('.textLayer').children().each(function() {
            $(this).html(undoHighliting($(this).html()));
        });
        dates = [];
        $('#cur_txt').off( "click" );
    });
    $('#cur_txt').click(function () {
        var start = this.selectionStart;
        for (var i=0; i<dates.length; i += 2) {
            if ((dates[i] <= start) && (dates[i+1] >= start)) {
                $(x).val(document.getElementById("cur_txt").innerHTML.slice(dates[i], dates[i+1]));
                $(pos).text('От ' + dates[i] + ' до ' + dates[i+1]);
                break;
            }
        }
        $('#containerPDF').off( "mouseup" );
        $('#hidden_text').html('');
        $('.textLayer').children().each(function() {
            $(this).html(undoHighliting($(this).html()));
        });
        dates = [];
        $('#cur_txt').off( "click" );
    });
}

function notInDoc(input, cb, label) {
    if (document.getElementById(cb).checked) {
        $(input).removeAttr('required')
        $(input).val('');
        $(input).prop('onclick', null);
        $(label).text('');
    } else {
        $(input).attr('required', 'required')
        $(input).attr('onclick', "javascript:getSel(' " + input + " ', ' " + label + "')");
    }
}

function setAdd(cb, label) {
    if (document.getElementById(cb).checked) {
        $(label).css("visibility", "visible");
    } else {
        $(label).css("visibility", "hidden");
    }
}

function timeUp() {
    
}

function startTimer() {
    var my_timer = document.getElementById("my_timer");
    var time = my_timer.innerHTML;
    var arr = time.split(":");
    var h = arr[0];
    var m = arr[1];
    var s = arr[2];
    if (s == 0) {
        if (m == 0) {
            if (h == 0) {
                timeUp();
                return;
            }
            h--;
            m = 60;
            if (h < 10) h = "0" + h;
        }
        m--;
        if (m < 10) m = "0" + m;
        s = 59;
    } else s--;
    if (s < 10) s = "0" + s;
    localStorage.setItem('timer', my_timer.innerHTML);
    document.getElementById("my_timer").innerHTML = h+":"+m+":"+s;
    t = setTimeout(startTimer, 1000);
}

function moveDiv() {
    var elmnt = document.getElementById("cur_txt");
    var y = elmnt.scrollTop;
    $('#hide').css('height',  $('#cur_txt').height() + y);
    $('#hide').css('top', -y-2);
}

function getDoc(url) {
    pdfjsLib.getDocument(url)
    .then(function(pdf) {
        var container = document.getElementById("containerPDF");
        var countPromises = [];
        for (var i = 1; i <= pdf.numPages; i++) {
            countPromises.push(pdf.getPage(i).then(function(page) {
            var scale = 1.1;
            var viewport = page.getViewport(scale);
            var div = document.createElement("div");
            div.setAttribute("id", "page-" + (page.pageIndex + 1));
            div.setAttribute("style", "position: relative");
            container.appendChild(div);
            var canvas = document.createElement("canvas");
            div.appendChild(canvas);
            var context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            var renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            return page.render(renderContext).then(function() {
                var textContent = page.getTextContent();
                return textContent.then(function(text) {
                    var textLayerDiv = document.createElement("div");
                    textLayerDiv.setAttribute("class", "textLayer");
                    div.appendChild(textLayerDiv);
                    var textLayer = new TextLayerBuilder({
                    textLayerDiv: textLayerDiv, 
                    pageIndex: page.pageIndex,
                    viewport: viewport
                    });
                    textLayer.setTextContent(text);
                    textLayer.render();
                    return text.items.map(function (s) { return s.str; }).join('');
                });
            });
        }));
    }
    Promise.all(countPromises).then(function (texts) {
        text = texts.join('');
        $('#cur_txt').text(text);
        $('#hidden_text').html(text);
    });
    });
}