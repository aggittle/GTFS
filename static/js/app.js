$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    $('form').submit(function(){
    socket.emit('form submit', {'stop':$('#stops').val(), 'direction':$('#direction').val()});
    return false;
    });
    //receive details from server
    socket.on('trip_updates', function(msg) {
        var updt = ''
        _update = msg.update;
        for (line in _update) {
          if (["A", "C", "E"].includes(line)){
            updt += '<span class="mta-ace mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          else if (["B", "D", "F", "M"].includes(line)){
            updt += '<span class="mta-bdfm mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          else if (["G"].includes(line)){
            updt += '<span class="mta-g mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          else if (["J", "Z"].includes(line)){
            updt += '<span class="mta-jz mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          else if (["L"].includes(line)){
            updt += '<span class="mta-l mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          else if (["N", "Q", "R"].includes(line)){
            updt += '<span class="mta-nqr mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          else if (["S"].includes(line)){
            updt += '<span class="mta-s mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          else if (["1", "2", "3"].includes(line)){
            updt += '<span class="mta-123 mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          else if (["4", "5", "6"].includes(line)){
            updt += '<span class="mta-456 mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          else if (["7"].includes(line)){
            updt += '<span class="mta-7 mta-bullet">' + line + '</span><br><p class = "mta">'+ _update[line] + '</p>'
          }
          };
        $('#updt').html(updt)
      });

    });
